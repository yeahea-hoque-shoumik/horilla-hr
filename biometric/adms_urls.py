"""
URLs for ADMS push devices, mounted at /iclock/.

Devices request these fixed paths; some firmware adds ``.aspx``.
"""

from django.urls import re_path

from . import adms

urlpatterns = [
    re_path(r"^cdata(?:\.aspx)?$", adms.cdata, name="adms-cdata"),
    re_path(r"^getrequest(?:\.aspx)?$", adms.getrequest, name="adms-getrequest"),
    re_path(r"^devicecmd(?:\.aspx)?$", adms.devicecmd, name="adms-devicecmd"),
    re_path(r"^ping(?:\.aspx)?$", adms.ping, name="adms-ping"),
]
