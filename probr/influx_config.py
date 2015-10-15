from django.conf import settings

influx_host = getattr(settings, "INFLUX_HOST", "localhost")

influx_port = getattr(settings, "INFLUX_PORT", "8086")

influx_user = getattr(settings, "INFLUX_USER", "root")

influx_pw = getattr(settings, "INFLUX_PW", "root")

influx_db = getattr(settings, "INFLUX_DB_NAME", "probr")