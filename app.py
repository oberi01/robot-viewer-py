import sys
from pathlib import Path
from robot.result import ExecutionResult
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Static, Label
from textual.containers import Horizontal, VerticalScroll, Container
from textual.binding import Binding

class RobotView(App):
    CSS = """
    Horizontal { height: 100%; }
    #list-container { width: 40%; border-right: solid $accent; }
    #detail-container { width: 60%; padding: 1; }
    .status-FAIL { color: $error; }
    .status-PASS { color: $success; }
    ListItem { padding: 0 1; }
    #status-bar {
        background: $accent;
        color: $text;
        width: 100%;
        padding: 0 1;
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Beenden"),
        Binding("a", "toggle_all", "Filter Alle/Fehler"),
    ]

    def __init__(self, xml_path):
        super().__init__()
        self.xml_path = xml_path
        self.show_all = False
        self.all_tests = []
        self.load_data()

    def load_data(self):
        """Liest die XML rekursiv ein, um Verschachtelungen auf Linux zu unterstützen"""
        result = ExecutionResult(self.xml_path)

        # Nutzt eine interne Hilfsfunktion für die Rekursion
        def _find_tests_rekursiv(suite):
            # 1. Füge alle Tests der aktuellen Ebene hinzu
            for test in suite.tests:
                self.all_tests.append(test)

            # 2. Gehe tiefer in alle Untersuites (Unterordner)
            for sub_suite in suite.suites:
                _find_tests_rekursiv(sub_suite)

        # Starte die Suche an der Wurzel der XML
        _find_tests_rekursiv(result.suite)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Container(id="list-container"):
                yield ListView(id="test-list")
                yield Label("Lade...", id="status-bar")
            with VerticalScroll(id="detail-container"):
                yield Static("Wähle einen Test...", id="detail-text")
        yield Footer()

    def on_mount(self):
        self.update_ui()

    def update_ui(self):
        list_view = self.query_one("#test-list", ListView)
        list_view.clear()
        
        visible = self.all_tests if self.show_all else [t for t in self.all_tests if not t.passed]

        # Update der Status-Zeile
        status_text = f" Gesamt: {len(self.all_tests)} | Sichtbar: {len(visible)}"
        if not self.show_all:
            status_text += " (nur Fehler)"

        self.query_one("#status-bar", Label).update(status_text)

        for test in visible:
            status_str = "FAIL" if not test.passed else "PASS"
            label = f"{test.name} [{status_str}]"
            item = ListItem(Label(label, classes=f"status-{status_str}"))
            item.test_data = test # Daten direkt ans Objekt hängen
            list_view.append(item)

    def action_toggle_all(self):
        self.show_all = not self.show_all
        self.update_ui()

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        """Update der Detailansicht beim Navigieren"""
        if event.item:
            test = event.item.test_data
            content = f"[b]Test:[/b] {test.full_name}\n"
            content += f"[b]Status:[/b] {test.status}\n\n"
            
            if test.message:
                content += f"[red][b]Fehlermeldung:[/b][/red]\n{test.message}\n\n"
            
            content += "[b]Keywords:[/b]\n"
            for kw in test.body:
                if hasattr(kw, 'name'):
                    color = "green" if kw.passed else "red"
                    content += f"- [{color}]{kw.name}[/{color}]\n"
            
            self.query_one("#detail-text", Static).update(content)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "output.xml"
    if not Path(path).exists():
        print(f"Datei nicht gefunden: {path}")
        sys.exit(1)
    
    app = RobotView(path)
    app.run()

if __name__ == "__main__":
    main()
