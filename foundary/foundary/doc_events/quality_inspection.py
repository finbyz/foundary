import frappe

def before_validate(self,method):
	update_manual_inspection(self)
	
def update_manual_inspection(self):
	for i in self.readings:
		if i.numeric == 0:
			i.manual_inspection = 1