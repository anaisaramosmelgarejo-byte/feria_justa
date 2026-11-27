import unittest
from matrices_feria import *
from catalogo import PRECIOS_EJEMPLO

# Precios fijos para estas pruebas: así no dependen de los precios reales del catálogo
PRECIOS_TEST = {"manzanas": 300, "platanos": 150, "zanahorias": 1200, "tomates": 1800, "paltas": 900}

EJ = [[4, 2, 1], [8, 4, 2], [12, 6, 3]]  # matriz del enunciado


class TestEstructura(unittest.TestCase):
    def test_dimensiones_base(self):
        self.assertEqual(dimensiones(crear_matriz_consumo()), (3, 5))

    def test_copia_independiente(self):
        m = crear_matriz_consumo(); m[0][0] = 999
        self.assertNotEqual(crear_matriz_consumo()[0][0], 999)

    def test_invalidas(self):
        for mala in ([], [[]], [[1, 2], [3]], [[1, -2]], [["a"]], "x"):
            with self.assertRaises(ErrorDeMatriz):
                validar_matriz(mala)


class TestAcceso(unittest.TestCase):
    def test_fila_y_columna(self):
        self.assertEqual(obtener_fila(EJ, 1), [8, 4, 2])
        self.assertEqual(obtener_columna(EJ, 0), [4, 8, 12])

    def test_por_nombre(self):
        m = crear_matriz_consumo()
        self.assertEqual(obtener_fila(m, "alto")[0], 3)
        self.assertEqual(obtener_columna(m, "manzanas"), [1, 2, 3])
        self.assertEqual(obtener_elemento(m, "medio", "platanos"), 3)


class TestOperaciones(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(sumar_matrices(EJ, EJ), [[8, 4, 2], [16, 8, 4], [24, 12, 6]])

    def test_suma_incompatible(self):
        with self.assertRaises(ErrorDeMatriz):
            sumar_matrices(EJ, [[1, 2], [3, 4]])

    def test_escalar(self):
        self.assertEqual(multiplicar_por_escalar(EJ, 2)[2], [24, 12, 6])
        self.assertEqual(multiplicar_por_escalar(EJ, 0)[0], [0, 0, 0])

    def test_escalar_invalido(self):
        with self.assertRaises(ErrorDeMatriz):
            multiplicar_por_escalar(EJ, -1)

    def test_resta_y_transpuesta(self):
        self.assertEqual(restar_matrices(EJ, EJ)[0], [0, 0, 0])
        self.assertEqual(transpuesta(EJ)[0], [4, 8, 12])
        self.assertEqual(dimensiones(transpuesta(crear_matriz_consumo())), (5, 3))

    def test_propiedad_distributiva(self):
        # k(A+B) == kA + kB
        self.assertEqual(multiplicar_por_escalar(sumar_matrices(EJ, EJ), 3),
                         sumar_matrices(multiplicar_por_escalar(EJ, 3),
                                        multiplicar_por_escalar(EJ, 3)))


class TestTotalesYComparacion(unittest.TestCase):
    def test_totales_producto(self):
        self.assertEqual(totales_por_producto(EJ), [24, 12, 6])

    def test_totales_escenario(self):
        self.assertEqual(totales_por_escenario(EJ), [7, 14, 21])

    def test_hogar(self):
        h = matriz_del_hogar(4)
        self.assertEqual(obtener_fila(h, "medio")[0], 8)  # 2 manzanas x 4

    def test_costo_por_escenario(self):
        h = matriz_del_hogar(4)
        costos = costo_por_escenario(h, PRECIOS_TEST)
        self.assertEqual(costos[1], 8*300 + 12*150 + 1.6*1200 + 2*1800 + 8*900)
        self.assertTrue(costos[0] < costos[1] < costos[2])

    def test_costo_vector_mal(self):
        with self.assertRaises(ErrorDeMatriz):
            costo_por_escenario(EJ, [1, 2])

    def test_comparar(self):
        d = comparar_escenarios(crear_matriz_consumo(), "bajo", "alto")
        self.assertEqual(d["manzanas"], 2)
        self.assertEqual(d["platanos"], 3)


if __name__ == "__main__":
    unittest.main()
