"""Pruebas de integración (Ana): logica.py conectando catalogo, funciones_calculo y matrices_feria."""
import unittest

import logica as lg


class TestIntegracion(unittest.TestCase):
    def test_lista_basica(self):
        # Ejemplo de la explicación matemática: 4 personas, medio, 3 manzanas en casa
        df, total, ev = lg.calcular_lista(["manzanas", "zanahorias"], "medio", 4,
                                          {"manzanas": 3}, {"manzanas": 300, "zanahorias": 1200}, 5000)
        self.assertEqual(total, 3420)
        self.assertTrue(ev["alcanza"])
        self.assertEqual(ev["diferencia"], 1580)
        self.assertEqual(list(df["Comprar"]), [5, 1.6])

    def test_stock_cubre_todo(self):
        df, total, ev = lg.calcular_lista(["manzanas"], "bajo", 2, {"manzanas": 50}, {"manzanas": 300}, 1000)
        self.assertEqual(total, 0)

    def test_entrada_invalida(self):
        with self.assertRaises(ValueError):
            lg.calcular_lista(["manzanas"], "medio", 0, {}, {"manzanas": 300}, 1000)

    def test_comparar(self):
        base, hogar, costos = lg.comparar(2, lg.PRECIOS_BASE)
        self.assertEqual(len(costos), 3)
        self.assertLess(costos[0], costos[2])

    def test_categorias_cubren_productos(self):
        self.assertEqual(sorted(lg.productos_de(lg.CATEGORIAS)), sorted(lg.PRODUCTOS))


if __name__ == "__main__":
    unittest.main()
