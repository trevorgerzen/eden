# -*- coding: utf-8 -*-

from gluon import current
from gluon.html import *
from gluon.storage import Storage

from s3.s3utils import S3CustomController

THEME = "Philippines"

# =============================================================================
class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):

        response = current.response
        
        output = {}
        #output["title"] = response.title = current.deployment_settings.get_system_name()

        s3 = response.s3
        # Image Carousel
        s3.jquery_ready.append('''$('#myCarousel').carousel()''')

        # Latest 4 Requests
        from s3.s3resource import S3FieldSelector
        s3db = current.s3db
        # Organisations
        s3.customize_org_needs_fields()
        layout = s3.render_org_needs # defined in config.py
        listid = "org_reqs"
        limit = 4
        list_fields = s3db.get_config("req_organisation_needs",
                                      "list_fields")


        resource = s3db.resource("req_organisation_needs")
        # Order with most recent first
        orderby = "date desc"
        output["org_reqs"] = latest_records(resource, layout, listid, limit, list_fields, orderby)

        # Sites
        s3.customize_site_needs_fields()
        layout = s3.render_site_needs # defined in config.py
        listid = "site_reqs"
        limit = 4
        list_fields = s3db.get_config("req_site_needs",
                                      "list_fields")

        resource = s3db.resource("req_site_needs")
        # Order with most recent first
        orderby = "date desc"
        output["site_reqs"] = latest_records(resource, layout, listid, limit, list_fields, orderby)

        self._view(THEME, "index.html")
        return output

# =============================================================================
def latest_records(resource, layout, listid, limit, list_fields, orderby):
    """
        Display a dataList of the latest records for a resource
    """

    #orderby = resource.table[orderby]
    datalist, numrows, ids = resource.datalist(fields=list_fields,
                                               start=None,
                                               limit=limit,
                                               listid=listid,
                                               orderby=orderby,
                                               layout=layout)
    if numrows == 0:
        # Empty table or just no match?
        from s3.s3crud import S3CRUD
        table = resource.table
        if "deleted" in table:
            available_records = current.db(table.deleted != True)
        else:
            available_records = current.db(table._id > 0)
        if available_records.select(table._id,
                                    limitby=(0, 1)).first():
            msg = DIV(S3CRUD.crud_string(resource.tablename,
                                         "msg_no_match"),
                      _class="empty")
        else:
            msg = DIV(S3CRUD.crud_string(resource.tablename,
                                         "msg_list_empty"),
                      _class="empty")
        data = msg
    else:
        # Render the list
        dl = datalist.html()
        data = dl

    return data

# =============================================================================
class time(S3CustomController):
    """ Custom page to display opportunities to donate Time """

    # -------------------------------------------------------------------------
    def __call__(self):
        """ Main entry point, configuration """

        self._view(THEME, "time.html")
        return dict()

# END =========================================================================
