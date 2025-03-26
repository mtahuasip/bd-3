from datetime import datetime


class Library:
    def __init__(self, carrera, facultad):
        self.carrera = carrera
        self.facultad = facultad
        self.createdAt = datetime.now()
        self.updatedAt = self.createdAt

    def to_collection(self):
        return {
            "carrera": self.carrera,
            "facultad": self.facultad,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
