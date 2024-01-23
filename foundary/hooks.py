from . import __version__ as app_version

app_name = "foundary"
app_title = "Foundary"
app_publisher = "Finbyz Tech PVT LTD"
app_description = "foundary app"
app_email = "info@finbyz.tech"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/foundary/css/foundary.css"
# app_include_js = "/assets/foundary/js/foundary.js"

# include js, css files in header of web template
# web_include_css = "/assets/foundary/css/foundary.css"
# web_include_js = "/assets/foundary/js/foundary.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "foundary/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Work Order" : "public/doc_js/work_order.js",
              "Job Card":"public/doc_js/job_card.js"}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
# from foundary.foundary.doc_events.stock_entry import check_if_operations_completed, set_process_loss_qty, get_scrap_items_from_job_card
# StockEntry.check_if_operations_completed = check_if_operations_completed
# StockEntry.set_process_loss_qty = set_process_loss_qty
# StockEntry.get_scrap_items_from_job_card = get_scrap_items_from_job_card

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "foundary.utils.jinja_methods",
#	"filters": "foundary.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "foundary.install.before_install"
# after_install = "foundary.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "foundary.uninstall.before_uninstall"
# after_uninstall = "foundary.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "foundary.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"BOM": "foundary.override.override_bom.CustomBOM",
    "Stock Entry": "foundary.foundary.doc_events.stock_entry.CustomStockEntry",
    # "Job Card": "foundary.foundary.doc_events.job_card.CustomJobCard",
    # "Work Order": "foundary.foundary.doc_events.work_order.CustomWorkOrder"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

doc_events = {
    "Job Card": {
		"on_update": "foundary.foundary.doc_events.job_card.on_update"
	},
	"Work Order": {
        "on_update": "foundary.foundary.doc_events.work_order.on_update",
        "on_update_after_submit": "foundary.foundary.doc_events.work_order.on_update_after_submit"
	},
    "Stock Entry": {
        "on_submit": "foundary.foundary.doc_events.stock_entry.on_submit"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
#	"all": [
#		"foundary.tasks.all"
#	],
	# "daily": [
	# 	"foundary.foundary.scheduler.repack_scrap_item.repack_stock_entry"
	# ],
#	"hourly": [
#		"foundary.tasks.hourly"
#	],
#	"weekly": [
#		"foundary.tasks.weekly"
#	],
#	"monthly": [
#		"foundary.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "foundary.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "foundary.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "foundary.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["foundary.utils.before_request"]
# after_request = ["foundary.utils.after_request"]

# Job Events
# ----------
# before_job = ["foundary.utils.before_job"]
# after_job = ["foundary.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"foundary.auth.validate"
# ]

from erpnext.manufacturing.report.job_card_summary import job_card_summary
from foundary.foundary.report.job_card_summary import execute
job_card_summary.execute = execute