from datetime import timedelta, datetime
from decimal import Decimal

from django.db import models
from django.db.utils import Error as dbError
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import transaction

from VeterinariaPatagonica.errores import VeterinariaPatagonicaError
from Apps.GestionDeServicios.models import Servicio
from Apps.GestionDeProductos.models import Producto
from .practica import *


__all__ = (
    "Estado", "Creada", "Presupuestada", "Programada",
    "Realizada", "RealizadaServicio", "RealizadaProducto",
    "Cancelada", "Facturada"
)


def verificarHabilitados(practica):

    if practica.cliente.baja:
        raise VeterinariaPatagonicaError(descripcion="El cliente con DNI/CUIT %s no se encuentra habilitado." % practica.cliente.dniCuit)
    if practica.mascota is not None and practica.mascota.baja:
        raise VeterinariaPatagonicaError(descripcion="La mascota con patente %s no se encuentra habilitada." % practica.mascota.patente)
    for detalle in practica.practica_servicios.all():
        if detalle.servicio.baja:
            raise VeterinariaPatagonicaError(descripcion="El servicio '%s' (%d) no se encuentra habilitado." % (detalle.servicio.nombre, detalle.servicio.id))
    for detalle in practica.practica_productos.all():
        if detalle.producto.baja:
            raise VeterinariaPatagonicaError(descripcion="El producto '%s' (%d) no se encuentra habilitado." % (detalle.producto.nombre, detalle.producto.id))


class EstadoManager(models.Manager):

    def inicializar(self, usuario):
        if hasattr(self, "instance") and (not self.instance is None):
            if self.get_queryset().count() == 0:
                creada = Creada(
                    usuario=usuario,
                    practica=self.instance
                )
                creada.save(force_insert=True)
            else:
                raise VeterinariaPatagonicaError(descripcion="La practica tiene estados asociados, no puede ser inicializada")
        else:
            raise VeterinariaPatagonicaError(descripcion="La practica a inicializar no es accesible desde el model manager")

    def inicial(self):
        if hasattr(self, "instance") and (not self.instance is None):
            queryset = self.get_queryset()
            if queryset.count() != 0:
                return queryset.get(tipo=Creada.TIPO)
            else:
                raise VeterinariaPatagonicaError(descripcion="La practica no fue inicializada, no tiene estados asociados")
        else:
            raise VeterinariaPatagonicaError(descripcion="La practica a inicializar no es accesible desde el model manager")

    def realizacion(self):
        if hasattr(self, "instance") and (not self.instance is None):
            queryset = self.get_queryset()
            if queryset.count() > 0:
                return queryset.get(tipo=Realizada.TIPO).related()
            else:
                raise VeterinariaPatagonicaError(descripcion="La practica no fue inicializada, no tiene estados asociados")
        else:
            raise VeterinariaPatagonicaError(descripcion="La practica a inicializar no es accesible desde el model manager")


class Estado(models.Model):

    class Meta:
        get_latest_by = "marca"
        default_permissions = ()

    TIPO = 0
    TIPOS = [
        (0, 'estado')
    ]

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

    def anotarPracticas(practicas, **kwargs):

        if kwargs.get("creada_por", False):
            estados = Estado.objects.filter(practica=models.OuterRef("id")).filter(tipo=Creada.TIPO)
            practicas = practicas.annotate(
                id_creada_por=models.Subquery(estados.values("usuario__id")[:1]),
                nombre_creada_por=models.Subquery(estados.values("usuario__username")[:1])
            )

        if kwargs.get("atendida_por", False):
            estados = Estado.objects.filter(practica=models.OuterRef("id")).order_by("-id")
            practicas = practicas.annotate(
                id_atendida_por=models.Subquery(estados.values("usuario__id")[:1]),
                nombre_atendida_por=models.Subquery(estados.values("usuario__username")[:1])
            )

        if kwargs.get("estado_actual", False):
            estados = Estado.objects.filter(practica=models.OuterRef("id")).order_by("-id")
            whens = [
                models.When( tipo_estado_actual=tipo[0], then=models.Value(tipo[1]) ) for tipo in Estado.TIPOS[1:]
            ]
            practicas = practicas.annotate(
                id_estado_actual=models.Subquery(estados.values("id")[:1]),
                tipo_estado_actual=models.Subquery(estados.values("tipo")[:1])
            ).annotate(
                nombre_estado_actual=models.Case(
                    *whens,
                    default=models.Value(""),
                    output_field=models.CharField()
                )
            )

        if kwargs.get("marca_ultima_actualizacion", False):
            practicas = practicas.annotate(
                marca_ultima_actualizacion=models.Max('estado__marca')
            )

        if kwargs.get("marca_creacion", False):
            practicas = practicas.annotate(
                marca_creacion=models.Min('estado__marca')
            )

        return practicas

    objects = EstadoManager()

    marca = models.DateTimeField(auto_now_add=True)

    practica = models.ForeignKey(
        Practica,
        related_name="estados",
        related_query_name="estado",
        on_delete=models.CASCADE
    )

    tipo = models.PositiveSmallIntegerField(choices=TIPOS)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    @staticmethod
    def actualizaciones():
        return set()

    @staticmethod
    def acciones():
        return set()

    def actualizacionesPosibles(self):
        if not self.esUltimo():
            return set()
        permitidas = self.practica.actualizaciones()
        return self.actualizaciones().intersection(permitidas)

    def accionesPosibles(self):
        permitidas = self.practica.acciones()
        retorno = self.acciones().intersection(permitidas)
        if not self.esUltimo():
            retorno = retorno - self.actualizacionesPosibles()
        return retorno

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Estado, self).save(*args, **kwargs)

    def related(self):
        return self.__class__ != Estado and self or getattr(self, self.get_tipo_display())

    def esUltimo(self):
        retorno = None
        actual = self.practica.estado()
        if actual:
            retorno = actual.id == self.related().id
        return retorno

    def esPrimero(self):
        retorno = None
        inicial = self.practica.estados.inicial()
        if inicial:
            retorno = inicial.id == self.related().id
        return retorno

    def siguienteEstado(self):
        retorno = Estado.objects.filter(
            practica=self.practica,
            id__gt=self.id
        ).order_by("id").first()
        if retorno is not None:
            retorno = retorno.related()
        return retorno

    def anteriorEstado(self):
        retorno = Estado.objects.filter(
            practica=self.practica,
            id__lt=self.id
        ).order_by("id").last()
        if retorno is not None:
            retorno = retorno.related()
        return retorno


    def fuePresupuestada(self):
        estados = self.practica.estados
        presupuestos = estados.filter(tipo=Presupuestada.TIPO)
        if presupuestos.count():
            return True
        return False

    def fueProgramada(self):
        estados = self.practica.estados
        turnos = estados.filter(tipo=Programada.TIPO)
        if turnos.count():
            return True
        return False

    def cotaInicio(self):
        retorno = None
        turnos = Programada.objects.filter(practica_id=self.practica.id).order_by("-id")
        if turnos.count():
            retorno = turnos[0].inicio
        else:
            presupuestos = Presupuestada.objects.filter(practica_id=self.practica.id).order_by("id")
            if presupuestos.count():
                retorno = presupuestos[0].marca
        return retorno

    def nombre(self):
        return str(self).lower()

    def __str__(self):
        return self.__class__.__name__


class EstadoCancelable(Estado):

    class Meta:
        abstract = True

    def cancelar(self, usuario, motivo=""):

        cancelada = Cancelada(
            usuario=usuario,
            practica=self.practica,
            motivo=motivo
        )
        cancelada.save(force_insert=True)
        return cancelada


class EstadoRealizable(Estado):

    class Meta:
        abstract = True

    def realizar(self, usuario, inicio, finalizacion, condicionPreviaMascota="", resultados=""):

        if self.practica.mascota is None:
            raise VeterinariaPatagonicaError(
                "Error",
                "La practica no tiene mascota"
            )

        if not self.practica.practica_servicios.count():
            raise VeterinariaPatagonicaError(
                "Error",
                "La practica no tiene servicios"
            )

        if not self.practica.practica_productos.count():
            raise VeterinariaPatagonicaError(
                "Error",
                "La practica no tiene productos"
            )

        fijarPrecios = self.fuePresupuestada()
        servicios = [
            RealizadaServicio(
                servicio=detalle.servicio,
                cantidad=detalle.cantidad,
                precio=detalle.precio if fijarPrecios else None,
            ) for detalle in self.practica.practica_servicios.all()
        ]
        productos = [
            RealizadaProducto(
                producto=detalle.producto,
                cantidad=detalle.cantidad,
                precio=detalle.precio if fijarPrecios else None,
            ) for detalle in self.practica.practica_productos.all()
        ]

        actualizacionStock = {
            detalle.producto.id : -detalle.cantidad for detalle in productos
        }

        cota = self.cotaInicio()
        if (cota is not None) and (inicio < cota):
            raise VeterinariaPatagonicaError(
                "Error",
                "La %s no puede tener inicio menor a las %s del %s" % (
                    self.practica.nombreTipo(),
                    cota.strftime("%H:%M"),
                    cota.strftime("%d/%m/%Y"),
                )
            )

        try:
            with transaction.atomic():
                realizada = Realizada(
                    usuario=usuario,
                    practica=self.practica,
                    inicio=inicio,
                    finalizacion=finalizacion,
                    condicionPreviaMascota=condicionPreviaMascota,
                    resultados=resultados,
                )
                realizada.save(force_insert=True)
                realizada.realizada_servicios.set(servicios, bulk=False)
                realizada.realizada_productos.set(productos, bulk=False)
                verificarHabilitados(self.practica)
                Producto.objects.actualizarStock(actualizacionStock)
        except dbError as excepcion:
            raise VeterinariaPatagonicaError(
                "Error en base de datos",
                "Ocurrio un error al intentar guardar los datos, la %s no pudo ser realizada" % self.practica.nombreTipo()
            )
        return realizada


class EstadoProgramable(Estado):

    class Meta:
        abstract = True

    def programar(self, usuario, inicio, finalizacion, adelanto):

        if self.practica.adelanto is not None:
            raise VeterinariaPatagonicaError(
                "Error",
                "La practica ya tiene adelanto registrado"
            )

        if self.practica.mascota is None:
            raise VeterinariaPatagonicaError(
                "Error",
                "La practica no tiene mascota"
            )

        ahora = datetime.now()
        try:
            with transaction.atomic():
                if inicio < ahora:
                    raise VeterinariaPatagonicaError(
                        "Error",
                        "La fecha y hora de programación de la %s no puede ser menor a las %s del %s" % (
                            self.practica.nombreTipo(),
                            ahora.strftime("%H:%M"),
                            ahora.strftime("%d/%m/%Y"),
                        )
                    )
                programada = Programada(
                    usuario=usuario,
                    practica=self.practica,
                    inicio=inicio,
                    finalizacion=finalizacion,
                )
                programada.save(force_insert=True)
                adelanto = Adelanto(
                    turno=programada,
                    importe=adelanto
                )
                adelanto.save(force_insert=True)
                self.practica.adelanto = adelanto
                self.practica.save(force_update=True)
                verificarHabilitados(self.practica)

        except dbError as excepcion:
            raise VeterinariaPatagonicaError(
                "Error en base de datos",
                "Ocurrio un error al intentar guardar los datos, la %s no pudo ser programada" % self.practica.nombreTipo()
            )
        return programada


class Creada(EstadoRealizable, EstadoCancelable, EstadoProgramable):
    TIPO = 1
    class Meta:
        permissions = (
            ("presupuestar_consulta_creada_atendida", "Permiso para presupuestar consultas en estado creada"),
            ("presupuestar_cirugia_creada_atendida", "Permiso para presupuestar cirugias en estado creada"),
            ("programar_cirugia_creada_atendida", "Permiso para programar cirugias en estado creada"),
            ("realizar_consulta_creada_atendida", "Permiso para realizar consultas en estado creada"),
            ("realizar_cirugia_creada_atendida", "Permiso para realizar cirugias en estado creada"),
            ("presupuestar_consulta_creada_no_atendida", "Permiso para presupuestar consultas en estado creada atendidas por otro usuario"),
            ("presupuestar_cirugia_creada_no_atendida", "Permiso para presupuestar cirugias en estado creada atendidas por otro usuario"),
            ("programar_cirugia_creada_no_atendida", "Permiso para programar cirugias en estado creada atendidas por otro usuario"),
            ("realizar_consulta_creada_no_atendida", "Permiso para realizar consultas en estado creada atendidas por otro usuario"),
            ("realizar_cirugia_creada_no_atendida", "Permiso para realizar cirugias en estado creada atendidas por otro usuario"),
            ("exportar_xlsx_consulta_creada_atendida", "Permiso para exportar en xlsx consultas creadas"),
            ("exportar_xlsx_consulta_creada_no_atendida", "Permiso para exportar en xlsx consultas creadas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_creada_atendida", "Permiso para exportar en xlsx cirugias creadas"),
            ("exportar_xlsx_cirugia_creada_no_atendida", "Permiso para exportar en xlsx cirugias creadas atendidas por otro usuario"),
        )
        default_permissions = ()

    @staticmethod
    def actualizaciones():
        return set()

    @staticmethod
    def acciones():
        return set()

    def presupuestar(self, usuario, diasMantenimiento):

        try:
            with transaction.atomic():
                presupuestada = Presupuestada(
                    usuario=usuario,
                    practica = self.practica,
                    diasMantenimiento=diasMantenimiento,
                )
                presupuestada.save(force_insert=True)
                verificarHabilitados(self.practica)
        except dbError as excepcion:
            raise VeterinariaPatagonicaError(
                "Error en base de datos",
                "Ocurrio un error al intentar guardar los datos, la %s no pudo ser presupuestada" % self.practica.nombreTipo()
            )

        return presupuestada


class ProgramadaManager(EstadoManager):
    def enHorario(self, inicio, finalizacion):

        total = models.Q(
            inicio__lte=inicio,
            finalizacion__gte=finalizacion
        )

        parcial = models.Q(
            inicio__gt=inicio,
            inicio__lt=finalizacion
        ) | models.Q(
            finalizacion__gt=inicio,
            finalizacion__lt=finalizacion
        )

        return self.annotate(
            max_id=models.Max('practica__estado__id')
        ).filter(
            total | parcial,
            id=models.F('max_id'),
        )


def intersectan(x, y):
    a = (y[0] <= x[0] <= y[1]) or (y[0] <= x[1] <= y[1])
    b = (x[0] <= y[0] <= x[1]) or (x[0] <= y[1] <= x[1])
    return a or b

def fusionar(x, y):
    a = min(x[0], y[0])
    b = max(x[1], y[1])
    return tuple([a, b])

class Programada(EstadoCancelable, EstadoRealizable):
    TIPO = 2
    class Meta:
        permissions = (
            ("reprogramar_cirugia_programada_atendida", "Permiso para reprogramar cirugias en estado programada"),
            ("reprogramar_cirugia_programada_no_atendida", "Permiso para reprogramar cirugias en estado programada atendidas por otro usuario"),
            ("realizar_cirugia_programada_atendida", "Permiso para realizar cirugias en estado programada"),
            ("realizar_cirugia_programada_no_atendida", "Permiso para realizar cirugias en estado programada atendidas por otro usuario"),
            ("cancelar_cirugia_programada_atendida", "Permiso para cancelar cirugias en estado programada"),
            ("cancelar_cirugia_programada_no_atendida", "Permiso para cancelar cirugias en estado programada atendidas por otro usuario"),
            ("listar_cirugia_programada_atendida", "Permiso para listar cirugias en estado programada"),
            ("listar_cirugia_programada_no_atendida", "Permiso para listar cirugias en estado programada atendidas por otro usuario"),
            ("ver_detalle_estado_cirugia_programada_atendida", "Permiso para ver informacion detallada de cirugias en estado programada"),
            ("ver_detalle_estado_cirugia_programada_no_atendida", "Permiso para ver informacion detallada de cirugias en estado programada atendidas por otro usuario"),
            ("exportar_xlsx_consulta_programada_atendida", "Permiso para exportar en xlsx consultas programadas"),
            ("exportar_xlsx_consulta_programada_no_atendida", "Permiso para exportar en xlsx consultas programadas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_programada_atendida", "Permiso para exportar en xlsx cirugias programadas"),
            ("exportar_xlsx_cirugia_programada_no_atendida", "Permiso para exportar en xlsx cirugias programadas atendidas por otro usuario"),
        )
        default_permissions = ()

    objects = ProgramadaManager()

    @staticmethod
    def actualizaciones():
        return set([
            Practica.Acciones.reprogramar,
            Practica.Acciones.realizar,
            Practica.Acciones.cancelar,
        ])

    @staticmethod
    def acciones():
        return set([
            Practica.Acciones.ver_informacion_general,
            Practica.Acciones.ver_detalle_estado,
            Practica.Acciones.listar,
        ]) | Programada.actualizaciones()

    @staticmethod
    def horariosOcupados(inicio, finalizacion):
        turnos = Programada.objects.enHorario(inicio, finalizacion)
        if not turnos.count():
            return []

        horarios = [ tuple([t.inicio, t.finalizacion]) for t in turnos ]
        nuevos = []

        fusiones = len(horarios)
        while fusiones:
            fusiones = 0
            horario = horarios.pop(0)

            while(len(horarios)):
                otro = horarios.pop(0)
                if intersectan(horario, otro):
                    horario = fusionar(horario, otro)
                    fusiones += 1
                else:
                    nuevos.append(otro)

            nuevos.insert(0,horario)
            horarios.extend(nuevos)
            nuevos.clear()

        return horarios

    @staticmethod
    def horariosDisponibles(inicio, finalizacion, minimo=None):
        disponibles = []
        ocupados = Programada.horariosOcupados(inicio, finalizacion)
        if len(ocupados) == 0:
            minimo = timedelta(0) if minimo is None else minimo
            if (finalizacion - inicio) >= minimo:
                return [ tuple([inicio, finalizacion]) ]
            else:
                return []

        for i in range(len(ocupados)-1):
            disponibles.append(tuple([ocupados[i][1], ocupados[i+1][0]]))

        if (inicio < ocupados[0][0]):
            disponibles.insert( 0, tuple([inicio, ocupados[0][0]]) )
        if (ocupados[-1][1] < finalizacion):
            disponibles.append( tuple([ocupados[-1][1], finalizacion]) )

        if (minimo is not None):
            return [ h for h in disponibles if ((h[1]-h[0]) >= minimo) ]
        else:
            return disponibles

    def anotarPracticas(practicas, **kwargs):
        practicas = Estado.anotarPracticas(practicas, **kwargs)

        turnos = Programada.objects.filter(practica=models.OuterRef("id")).order_by("-id")

        if kwargs.get("programada_por", False):
            practicas = practicas.annotate(
                id_programada_por=models.Subquery(turnos.values("usuario__id")[:1]),
                nombre_programada_por=models.Subquery(turnos.values("usuario__username")[:1])
            )

        if kwargs.get("horario_turno", False) or kwargs.get("duracion_turno", False):
            practicas = practicas.annotate(
                inicio_turno=models.Subquery(turnos.values("inicio")[:1])
            ).annotate(
                finalizacion_turno=models.Subquery(turnos.values("finalizacion")[:1])
            )

        if kwargs.get("duracion_turno", False):
            practicas = practicas.annotate(
                duracion_turno=models.ExpressionWrapper(
                    models.F("finalizacion_turno") - models.F("inicio_turno"),
                    models.DurationField()
                )
            )

        if kwargs.get("reprogramaciones", False):
            practicas = practicas.annotate(
                reprogramaciones=models.ExpressionWrapper(
                    models.Count("estado__programada") - 1,
                    models.IntegerField()
                )
            )

        return practicas

    inicio = models.DateTimeField()

    finalizacion = models.DateTimeField()

    motivoReprogramacion = models.CharField(
        verbose_name="Motivo de reprogramacion",
        max_length=Practica.MAX_MOTIVO,
        blank=True,
    )

    def reprogramar(self, usuario, inicio, finalizacion, motivoReprogramacion=""):
        ahora = datetime.now()
        if inicio < ahora:
            raise VeterinariaPatagonicaError(
                "Error",
                "La fecha y hora de programación de la %s no puede ser menor a las %s del %s" % (
                    self.practica.nombreTipo(),
                    ahora.strftime("%H:%M"),
                    ahora.strftime("%d/%m/%Y"),
                )
            )
        programada = Programada(
            usuario=usuario,
            practica=self.practica,
            inicio=inicio,
            finalizacion=finalizacion,
            motivoReprogramacion=motivoReprogramacion
        )
        programada.save(force_insert=True)
        return programada

    def duracion(self):
        return int((self.finalizacion-self.inicio).total_seconds() / 60)

    def esReprogramacion(self):
        return isinstance(self.anteriorEstado(), Programada)

    def fueRealizado(self):
        siguienteEstado = self.siguienteEstado()
        if siguienteEstado is None:
            return False
        if isinstance(siguienteEstado.related(), Realizada):
            return True
        return False

    def fueCancelado(self):
        siguiente = self.siguienteEstado()
        if siguiente is None:
            return False
        return isinstance(siguiente, Cancelada)

    def fueReprogramado(self):
        siguiente = self.siguienteEstado()
        if siguiente is None:
            return False
        return isinstance(siguiente, Programada)

    def tiempoRestante(self):
        retorno = timedelta()
        tiempo = self.inicio - datetime.now()
        if (tiempo > retorno):
            retorno = tiempo
        return retorno

    def turnosMismoHorario(self):
        return Programada.objects.enHorario(
            self.inicio,
            self.finalizacion,
        ).exclude(id=self.id)


class Presupuestada(EstadoRealizable, EstadoProgramable):
    TIPO = 3
    class Meta:
        permissions = (
            ("realizar_consulta_presupuestada_atendida", "Permiso para realizar consultas en estado presupuestada"),
            ("realizar_consulta_presupuestada_no_atendida", "Permiso para realizar consultas en estado presupuestada atendidas por otro usuario"),
            ("realizar_cirugia_presupuestada_atendida", "Permiso para realizar cirugias en estado presupuestada"),
            ("realizar_cirugia_presupuestada_no_atendida", "Permiso para realizar cirugias en estado presupuestada atendidas por otro usuario"),
            ("programar_cirugia_presupuestada_atendida", "Permiso para programar cirugias en estado presupuestada"),
            ("programar_cirugia_presupuestada_no_atendida", "Permiso para programar cirugias en estado presupuestada atendidas por otro usuario"),
            ("listar_consulta_presupuestada_atendida", "Permiso para listar consultas en estado presupuestada"),
            ("listar_consulta_presupuestada_no_atendida", "Permiso para listar consultas en estado presupuestada atendidas por otro usuario"),
            ("listar_cirugia_presupuestada_atendida", "Permiso para listar cirugias en estado presupuestada"),
            ("listar_cirugia_presupuestada_no_atendida", "Permiso para listar cirugias en estado presupuestada atendidas por otro usuario"),
            ("ver_detalle_estado_consulta_presupuestada_atendida", "Permiso para ver informacion detallada de consultas en estado presupuestada"),
            ("ver_detalle_estado_consulta_presupuestada_no_atendida", "Permiso para ver informacion detallada de consultas en estado presupuestada atendidas por otro usuario"),
            ("ver_detalle_estado_cirugia_presupuestada_atendida", "Permiso para ver informacion detallada de cirugias en estado presupuestada"),
            ("ver_detalle_estado_cirugia_presupuestada_no_atendida", "Permiso para ver informacion detallada de cirugias en estado presupuestada atendidas por otro usuario"),
            ("exportar_xlsx_consulta_presupuestada_atendida", "Permiso para exportar en xlsx consultas presupuestadas"),
            ("exportar_xlsx_consulta_presupuestada_no_atendida", "Permiso para exportar en xlsx consultas presupuestadas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_presupuestada_atendida", "Permiso para exportar en xlsx cirugias presupuestadas"),
            ("exportar_xlsx_cirugia_presupuestada_no_atendida", "Permiso para exportar en xlsx cirugias presupuestadas atendidas por otro usuario"),
        )
        default_permissions = ()

    @staticmethod
    def actualizaciones():
        return set([
            Practica.Acciones.programar,
            Practica.Acciones.realizar,
        ])

    @staticmethod
    def acciones():
        return set([
            Practica.Acciones.ver_informacion_general,
            Practica.Acciones.ver_detalle_estado,
            Practica.Acciones.listar,
        ]) | Presupuestada.actualizaciones()


    diasMantenimiento = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1,"Los dias de mantenimiento del presupuesto deben ser mas que cero")
        ],
    )

    def vencimiento(self):
        return self.marca.date() + timedelta(days=self.diasMantenimiento)

    def diasVigencia(self):
        if not self.esUltimo():
            return 0
        dias = (self.vencimiento() - datetime.now().date()).days
        return int( max(dias,0) )

    def fueConfirmado(self):
        siguiente = self.siguienteEstado()
        if siguiente is None:
            return False
        return isinstance(siguiente, (Programada, Realizada))

    def haExpirado(self):
        return (self.diasVigencia() == 0) and (not self.fueConfirmado())

    def estaCompleto(self):
        return not (
            self.practica.cliente is None or self.practica.mascota is None
        )

    def accionesPosibles(self):
        if (self.diasVigencia() == 0):
            return set()
        return super().accionesPosibles()

    def programar(self, *args, **kwargs):
        if self.haExpirado():
            raise VeterinariaPatagonicaError(
                "Error",
                "El presupuesto no se puede programar, ya ha expirado"
            )
        super().programar(*args, **kwargs)

    def realizar(self, *args, **kwargs):
        if self.haExpirado():
            raise VeterinariaPatagonicaError(
                "Error",
                "El presupuesto no se puede realizar, ya ha expirado"
            )
        super().realizar(*args, **kwargs)


class Realizada(Estado):
    TIPO = 5
    class Meta:
        permissions = (
            ("facturar_consulta_realizada_atendida", "Permiso para facturar consultas en estado realizada"),
            ("facturar_consulta_realizada_no_atendida", "Permiso para facturar consultas en estado realizada atendidas por otro usuario"),
            ("facturar_cirugia_realizada_atendida", "Permiso para facturar cirugias en estado realizada"),
            ("facturar_cirugia_realizada_no_atendida", "Permiso para facturar cirugias en estado realizada atendidas por otro usuario"),
            ("modificar_consulta_realizada_atendida", "Permiso para modificar consultas en estado realizada"),
            ("modificar_consulta_realizada_no_atendida", "Permiso para modificar consultas en estado realizada atendidas por otro usuario"),
            ("modificar_cirugia_realizada_atendida", "Permiso para modificar cirugias en estado realizada"),
            ("modificar_cirugia_realizada_no_atendida", "Permiso para modificar cirugias en estado realizada atendidas por otro usuario"),
            ("modificar_informacion_clinica_consulta_realizada_atendida", "Permiso para modificar informacion clinica de consultas"),
            ("modificar_informacion_clinica_consulta_realizada_no_atendida", "Permiso para modificar informacion clinica de consultas atendidas por otro usuario"),
            ("modificar_informacion_clinica_cirugia_realizada_atendida", "Permiso para modificar informacion clinica de cirugias"),
            ("modificar_informacion_clinica_cirugia_realizada_no_atendida", "Permiso para modificar informacion clinica de cirugias atendidas por otro usuario"),
            ("listar_consulta_realizada_atendida", "Permiso para listar consultas en estado realizada"),
            ("listar_consulta_realizada_no_atendida", "Permiso para listar consultas en estado realizada atendidas por otro usuario"),
            ("listar_cirugia_realizada_atendida", "Permiso para listar cirugias en estado realizada"),
            ("listar_cirugia_realizada_no_atendida", "Permiso para listar cirugias en estado realizada atendidas por otro usuario"),
            ("ver_informacion_clinica_consulta_realizada_atendida", "Permiso para ver informacion clinica de consultas"),
            ("ver_informacion_clinica_consulta_realizada_no_atendida", "Permiso para ver informacion clinica de consultas atendidas por otro usuario"),
            ("ver_informacion_clinica_cirugia_realizada_atendida", "Permiso para ver informacion clinica de cirugias"),
            ("ver_informacion_clinica_cirugia_realizada_no_atendida", "Permiso para ver informacion clinica de cirugias atendidas por otro usuario"),
            ("ver_detalle_estado_consulta_realizada_atendida", "Permiso para ver informacion detallada de consultas en estado realizada"),
            ("ver_detalle_estado_consulta_realizada_no_atendida", "Permiso para ver informacion detallada de consultas en estado realizada atendidas por otro usuario"),
            ("ver_detalle_estado_cirugia_realizada_atendida", "Permiso para ver informacion detallada de cirugias en estado realizada"),
            ("ver_detalle_estado_cirugia_realizada_no_atendida", "Permiso para ver informacion detallada de cirugias en estado realizada atendidas por otro usuario"),
            ("exportar_xlsx_consulta_realizada_atendida", "Permiso para exportar en xlsx consultas realizadas"),
            ("exportar_xlsx_consulta_realizada_no_atendida", "Permiso para exportar en xlsx consultas realizadas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_realizada_atendida", "Permiso para exportar en xlsx cirugias realizadas"),
            ("exportar_xlsx_cirugia_realizada_no_atendida", "Permiso para exportar en xlsx cirugias realizadas atendidas por otro usuario"),
        )
        default_permissions = ()

    @staticmethod
    def actualizaciones():
        return set([
            Practica.Acciones.facturar,
        ])

    @staticmethod
    def acciones():
        return set([
            Practica.Acciones.listar,
            Practica.Acciones.ver_informacion_general,
            Practica.Acciones.ver_detalle_estado,
            Practica.Acciones.modificar,
            Practica.Acciones.ver_informacion_clinica,
            Practica.Acciones.modificar_informacion_clinica,
        ]) | Realizada.actualizaciones()


    def anotarPracticas(practicas, **kwargs):
        practicas = Estado.anotarPracticas(practicas, **kwargs)

        realizaciones = Realizada.objects.filter(practica=models.OuterRef("id")).order_by("-id")

        if kwargs.get("realizada_por", False):
            practicas = practicas.annotate(
                id_realizada_por=models.Subquery(realizaciones.values("usuario__id")[:1]),
                nombre_realizada_por=models.Subquery(realizaciones.values("usuario__username")[:1])
            )

        if kwargs.get("horario_realizacion", False) or kwargs.get("duracion_realizacion", False):
            practicas = practicas.annotate(
                inicio_realizacion=models.Subquery(realizaciones.values("inicio")[:1])
            ).annotate(
                finalizacion_realizacion=models.Subquery(realizaciones.values("finalizacion")[:1])
            )

        if kwargs.get("duracion_realizacion", False):
            practicas = practicas.annotate(
                duracion_realizacion=models.ExpressionWrapper(
                    models.F("finalizacion_realizacion") - models.F("inicio_realizacion"),
                    models.DurationField()
                )
            )

        return practicas

    inicio = models.DateTimeField()

    finalizacion = models.DateTimeField()

    condicionPreviaMascota = models.TextField(
        blank=True
    )

    resultados = models.TextField(
        blank=True
    )

    servicios = models.ManyToManyField(
        Servicio,
        through='RealizadaServicio',
        through_fields=('realizada','servicio'),
        related_name='realizadas',
        related_query_name='practica_realizada',
    )

    productos = models.ManyToManyField(
        Producto,
        through='RealizadaProducto',
        through_fields=('realizada','producto'),
        related_name='realizadas',
        related_query_name='practica_realizada',
    )

    def facturar(self, usuario):
        if self.practica.precio is not None:
            raise VeterinariaPatagonicaError(
                "Error",
                "No se puede facturar la %s, ya tiene precio" % self.practica.nombreTipo()
            )
        try:
            with transaction.atomic():
                if not self.fuePresupuestada():
                    for detalle in self.realizada_servicios.all():
                        detalle.precio = detalle.servicio.precioManoDeObra
                        detalle.save()
                    for detalle in self.realizada_productos.all():
                        detalle.precio = detalle.producto.precioDeCompra
                        detalle.save()
                facturada = Facturada(
                    usuario=usuario,
                    practica=self.practica
                )
                facturada.save(force_insert=True)
                self.completarPrecio()
        except dbError as error:
            raise VeterinariaPatagonicaError(
                "Error",
                "Ocurrio un error al intentar guardar los datos, la %s no pudo ser facturada" % self.practica.nombreTipo()
            )
        return facturada

    def duracion(self):
        return int((self.finalizacion-self.inicio).total_seconds() / 60)

    def importeServicios(self):
        return sum([
            detalle.precioTotal() for detalle in self.realizada_servicios.all()
        ])

    def importeProductos(self):
        return sum([
            detalle.precioTotal() for detalle in self.realizada_productos.all()
        ])

    def ajusteServicios(self):
        return self.importeServicios() * self.practica.tipoDeAtencion.recargo / Decimal(100)


    def ajusteProductos(self):
        return self.importeProductos() * self.practica.tipoDeAtencion.recargo / Decimal(100)

    def totalServicios(self):
        servicios = [ detalle for detalle in self.realizada_servicios.all() ]
        total = sum([ detalle.precioTotal() for detalle in servicios ])
        ajuste = total * self.practica.tipoDeAtencion.recargo / Decimal(100)
        return total + ajuste

    def totalProductos(self):
        productos = [ detalle for detalle in self.realizada_productos.all() ]
        total = sum([ detalle.precioTotal() for detalle in productos ])
        ajuste = total * self.practica.tipoDeAtencion.recargo / Decimal(100)
        return total + ajuste

    def total(self):
        return self.totalProductos() + self.totalServicios()

    def completarPrecio(self):
        practica = self.practica
        practica.precio = self.total()
        practica.save(force_update=True)

    def serviciosFijos(self):
        x = self.practica.practica_servicios.count()
        return self.realizada_servicios.all()[0:x]

    def productosFijos(self):
        x = self.practica.practica_productos.count()
        return self.realizada_productos.all()[0:x]

    def accionesPosibles(self):
        retorno = super().accionesPosibles()
        if self.fuePresupuestada():
            retorno -= set( [Practica.Acciones.modificar] )
        return retorno


class RealizadaServicio(models.Model):

    class Meta:
        default_permissions = ()

    realizada = models.ForeignKey(
        Realizada,
        on_delete=models.CASCADE,
        related_name='realizada_servicios'
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='servicio_realizadas'
    )

    cantidad = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1,"La cantidad debe ser mayor que cero")
        ],
    )

    precio = models.DecimalField(
        null=True,
        blank=True,
        max_digits=Practica.MAX_DIGITOS,
        decimal_places=Practica.MAX_DECIMALES,
        validators = [
            MinValueValidator(
                Practica.MIN_PRECIO,
                message=("El precio no puede ser menor a {:.%df}" % (Practica.MAX_DECIMALES)).format(Practica.MIN_PRECIO)
            ),
        ]
    )

    observaciones = models.TextField(
        blank=True
    )

    def precioTotal(self):
        if self.precio is not None:
            precio = self.precio
        else:
            precio = self.servicio.precioManoDeObra
        return self.cantidad * precio


class RealizadaProducto(models.Model):

    class Meta:
        default_permissions = ()

    realizada = models.ForeignKey(
        Realizada,
        on_delete=models.CASCADE,
        related_name='realizada_productos'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='producto_realizadas'
    )

    cantidad = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1,"La cantidad debe ser mayor que cero")
        ],
    )

    precio = models.DecimalField(
        null=True,
        blank=True,
        max_digits=Practica.MAX_DIGITOS,
        decimal_places=Practica.MAX_DECIMALES,
        validators = [
            MinValueValidator(
                Practica.MIN_PRECIO,
                message=("El precio no puede ser menor a {:.%df}" % (Practica.MAX_DECIMALES)).format(Practica.MIN_PRECIO)
            ),
        ]
    )

    def precioTotal(self):
        if self.precio is not None:
            precio = self.precio
        else:
            precio = self.producto.precioDeCompra
        return self.cantidad * precio


class Cancelada(Estado):
    TIPO = 4
    class Meta:
        permissions = (
            ("listar_cirugia_cancelada_atendida", "Permiso para listar cirugias en estado cancelada"),
            ("listar_cirugia_cancelada_no_atendida", "Permiso para listar cirugias en estado cancelada atendidas por otro usuario"),
            ("ver_detalle_estado_cirugia_cancelada_atendida", "Permiso para ver informacion detallada de cirugias en estado cancelada"),
            ("ver_detalle_estado_cirugia_cancelada_no_atendida", "Permiso para ver informacion detallada de cirugias en estado cancelada atendidas por otro usuario"),
            ("exportar_xlsx_consulta_cancelada_atendida", "Permiso para exportar en xlsx consultas canceladas"),
            ("exportar_xlsx_consulta_cancelada_no_atendida", "Permiso para exportar en xlsx consultas canceladas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_cancelada_atendida", "Permiso para exportar en xlsx cirugias canceladas"),
            ("exportar_xlsx_cirugia_cancelada_no_atendida", "Permiso para exportar en xlsx cirugias canceladas atendidas por otro usuario"),
        )
        default_permissions = ()

    motivo = models.TextField(
        blank=True
    )

    @staticmethod
    def acciones():
        return set([
            Practica.Acciones.listar,
            Practica.Acciones.ver_informacion_general,
            Practica.Acciones.ver_detalle_estado,
        ])


class Facturada(Estado):
    TIPO = 6
    class Meta:
        permissions = (
            ("listar_consulta_facturada_atendida", "Permiso para listar consultas en estado facturada"),
            ("listar_consulta_facturada_no_atendida", "Permiso para listar consultas en estado facturada atendidas por otro usuario"),
            ("listar_cirugia_facturada_atendida", "Permiso para listar cirugias en estado facturada"),
            ("listar_cirugia_facturada_no_atendida", "Permiso para listar cirugias en estado facturada atendidas por otro usuario"),
            ("ver_detalle_estado_consulta_facturada_atendida", "Permiso para ver informacion detallada de consultas en estado facturada"),
            ("ver_detalle_estado_consulta_facturada_no_atendida", "Permiso para ver informacion detallada de consultas en estado facturada atendidas por otro usuario"),
            ("ver_detalle_estado_cirugia_facturada_atendida", "Permiso para ver informacion detallada de cirugias en estado facturada"),
            ("ver_detalle_estado_cirugia_facturada_no_atendida", "Permiso para ver informacion detallada de cirugias en estado facturada atendidas por otro usuario"),
            ("ver_informacion_clinica_consulta_facturada_atendida", "Permiso para ver informacion clinica de consultas"),
            ("ver_informacion_clinica_consulta_facturada_no_atendida", "Permiso para ver informacion clinica de consultas atendidas por otro usuario"),
            ("ver_informacion_clinica_cirugia_facturada_atendida", "Permiso para ver informacion clinica de cirugias"),
            ("ver_informacion_clinica_cirugia_facturada_no_atendida", "Permiso para ver informacion clinica de cirugias atendidas por otro usuario"),
            ("exportar_xlsx_consulta_facturada_atendida", "Permiso para exportar en xlsx consultas facturadas"),
            ("exportar_xlsx_consulta_facturada_no_atendida", "Permiso para exportar en xlsx consultas facturadas atendidas por otro usuario"),
            ("exportar_xlsx_cirugia_facturada_atendida", "Permiso para exportar en xlsx cirugias facturadas"),
            ("exportar_xlsx_cirugia_facturada_no_atendida", "Permiso para exportar en xlsx cirugias facturadas atendidas por otro usuario"),
        )
        default_permissions = ()

    @staticmethod
    def acciones():
        return set([
            Practica.Acciones.listar,
            Practica.Acciones.ver_informacion_general,
            Practica.Acciones.ver_detalle_estado,
            Practica.Acciones.ver_informacion_clinica,
        ])


for Klass in (Creada, Presupuestada, Programada, Realizada, Facturada, Cancelada):
    Estado.register(Klass)
