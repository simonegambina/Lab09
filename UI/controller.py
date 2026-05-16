import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_analizza(self, e):
        self._view.txt_result.controls.clear()

        distanza = self._view.txt_distance.value

        if distanza is None or distanza.strip() == "":
            self._view.create_alert("Inserire una distanza minima")
            return

        try:
            distanza = float(distanza)
        except ValueError:
            self._view.create_alert("La distanza deve essere un numero")
            return

        if distanza < 0:
            self._view.create_alert("La distanza deve essere positiva")
            return

        self._model.build_graph(distanza)

        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()

        self._view.txt_result.controls.append(
            ft.Text(f"Numero vertici: {num_nodi}", size=18)
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {num_archi}", size=18)
        )

        self._view.txt_result.controls.append(
            ft.Text("Elenco archi:", size=18, weight=ft.FontWeight.BOLD)
        )

        edges = self._model.get_edges()

        if len(edges) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun arco trovato con questa distanza minima.")
            )
        else:
            for iata1, airport1, iata2, airport2, distance in edges:
                self._view.txt_result.controls.append(
                    ft.Text(
                        f"{iata1} - {iata2} | "
                        f"{airport1} - {airport2} | "
                        f"distanza media: {distance:.2f} miglia"
                    )
                )

        self._view.update_page()