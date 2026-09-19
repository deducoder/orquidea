from orquidea.catalogo.modelo import Especie
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo


def fuentes_de(especie: Especie) -> list[str]:
    cuidados = especie.cuidados
    return [
        *especie.fuentes,
        cuidados.luz.fuente,
        cuidados.riego.fuente,
        cuidados.temperatura.fuente,
        cuidados.sustrato.fuente,
    ]


def test_el_catalogo_real_tiene_al_menos_cien_especies() -> None:
    assert len(cargar_catalogo(DIRECTORIO_CATALOGO)) >= 100


def test_toda_fuente_del_catalogo_real_trae_url_y_fecha_de_consulta() -> None:
    for especie in cargar_catalogo(DIRECTORIO_CATALOGO):
        for fuente in fuentes_de(especie):
            assert "https://" in fuente, (especie.id, fuente)
            assert "consultada el" in fuente, (especie.id, fuente)


def test_los_cuidados_de_genero_lo_dicen() -> None:
    for especie in cargar_catalogo(DIRECTORIO_CATALOGO):
        for cuidado in vars(especie.cuidados).values():
            assert "no específico de la especie" in cuidado.fuente or "medido" in cuidado.fuente


def test_guarianthe_cita_la_hoja_de_cattleya_y_lo_dice() -> None:
    especies = {e.id: e for e in cargar_catalogo(DIRECTORIO_CATALOGO)}
    fuente = especies["guarianthe-skinneri"].cuidados.riego.fuente

    assert "Cattleya Culture Sheet" in fuente
    assert "no tiene hoja para Guarianthe" in fuente
