from pydantic import BaseModel


class ConversionParams(BaseModel):
    g_signals: list[str] = ['L1C', 'C1C']
    e_signals: list[str] = ['L1C', 'C1C']
    c_signals: list[str] = ['L2I', 'C2I']
    r_signals: list[str] = ['L1C', 'C1C']
    s_signals: list[str] = []
    timestep: int = 30

    def get_signal_by_system(self):
        signal = {'G': self.g_signals,
                  'R': self.r_signals,
                  'E': self.e_signals,
                  'C': self.c_signals,
                  'S': self.s_signals}
        return signal