class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        # return "{:04d}".format(value)
        return f"{value:04d}"
        # return "%04d" % value
