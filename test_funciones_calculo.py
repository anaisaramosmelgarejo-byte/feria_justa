import unittest
from funciones_calculo import *
from catalogo import PRECIOS_EJEMPLO

# Precios fijos para estas pruebas: así no dependen de los precios reales del catálogo
PRECIOS_TEST = {"manzanas": 300, "platanos": 150, "zanahorias": 1200, "tomates": 1800, "paltas": 900}


class TestCantidades(unittest.TestCase):
    def test_ejemplo_enunciado(self):
        self.assertEqual(calcular_cantidad_semanal(2, 4), 8)

    def test_con_frecuencia(self):
        self.assertEqual(calcular_cantidad_semanal(1, 3, 2), 6)

    def test_cero_integrantes(self):
        self.assertEqual(calcular_cantidad_semanal(2, 0), 0)

    def test_por_escenario(self):
        self.assertEqual(calcular_cantidad_por_escenario("manzanas", "medio", 4), 8)
        self.assertAlmostEqual(calcular_cantidad_por_escenario("zanahorias", "alto", 3), 1.8)


class TestValidacion(unittest.TestCase):
    def test_negativos(self):
        with self.assertRaises(ErrorDeValidacion):
            calcular_cantidad_semanal(-1, 4)
        with self.assertRaises(ErrorDeValidacion):
            calcular_cantidad_semanal(2, -3)

    def test_tipos_invalidos(self):
        for malo in ("a", None, True, float("nan"), float("inf")):
            with self.assertRaises(ErrorDeValidacion):
                validar_numero(malo)

    def test_integrantes_no_entero(self):
        with self.assertRaises(ErrorDeValidacion):
            calcular_cantidad_semanal(2, 2.5)

    def test_producto_escenario_invalidos(self):
        with self.assertRaises(ErrorDeValidacion):
            calcular_cantidad_por_escenario("pizza", "bajo", 2)
        with self.assertRaises(ErrorDeValidacion):
            calcular_cantidad_por_escenario("manzanas", "extremo", 2)


class TestExistenciasYRedondeo(unittest.TestCase):
    def test_descuento(self):
        self.assertEqual(descontar_existencias(8, 3), 5)

    def test_existencia_mayor_no_es_negativo(self):
        self.assertEqual(descontar_existencias(8, 20), 0)

    def test_redondeo_unidades(self):
        self.assertEqual(redondear_compra(2.1, "unidades"), 3)
        self.assertEqual(redondear_compra(2, "unidades"), 2)

    def test_redondeo_kg(self):
        self.assertEqual(redondear_compra(0.85, "kg"), 0.9)
        self.assertEqual(redondear_compra(1.2, "kg"), 1.2)  # sin error de flotantes


class TestCostos(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(calcular_subtotal(5, 300), 1500)

    def test_total(self):
        self.assertEqual(calcular_total([1500, 800, 0]), 2300)

    def test_total_vacio(self):
        self.assertEqual(calcular_total([]), 0)

    def test_presupuesto(self):
        self.assertTrue(evaluar_presupuesto(2300, 3000)["alcanza"])
        r = evaluar_presupuesto(3500, 3000)
        self.assertFalse(r["alcanza"])
        self.assertEqual(r["diferencia"], -500)


class TestListaCompras(unittest.TestCase):
    def test_lista_completa(self):
        r = generar_lista_compras(4, "medio", ["manzanas", "zanahorias"],
                                  PRECIOS_TEST, existencias={"manzanas": 3},
                                  presupuesto=5000)
        m, z = r["items"]
        self.assertEqual(m["necesaria"], 8)
        self.assertEqual(m["a_comprar"], 5)
        self.assertEqual(m["subtotal"], 1500)
        self.assertEqual(z["a_comprar"], 1.6)
        self.assertEqual(z["subtotal"], 1920)
        self.assertEqual(r["total"], 3420)
        self.assertTrue(r["presupuesto"]["alcanza"])

    def test_sin_integrantes(self):
        with self.assertRaises(ErrorDeValidacion):
            generar_lista_compras(0, "bajo", ["manzanas"], PRECIOS_EJEMPLO)

    def test_falta_precio(self):
        with self.assertRaises(ErrorDeValidacion):
            generar_lista_compras(2, "bajo", ["manzanas"], {})


if __name__ == "__main__":
    unittest.main()
