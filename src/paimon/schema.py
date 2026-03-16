from dataclasses import dataclass

@dataclass
class DataItem:
    text: str
    color: str = "white"
    tooltip: str | None = None

    def __str__(self):
        return self.text


@dataclass
class NetResult:
    ok: bool
    latency: float | None
    status: str

    def text(self):

        if self.ok:
            return f"{self.latency:.0f} ms"

        return self.status

    def color(self, threshold=(50, 100)):

        if not self.ok:
            return "red"

        green, warn = threshold

        if self.latency < green:
            return "lime"

        if self.latency < warn:
            return "orange"

        return "red"