import frappe
import pyqrcode
import json

SUCCESS = 200
NOT_FOUND = 400

@frappe.whitelist(allow_guest=True)
def get_all_items(group):
    #group = "Consumable"
    #items = frappe.db.sql(f"""SELECT 
    #name, item_name, description
    #FROM `tabItem` 
    #WHERE item_group='{group}';""", as_dict=True)

    items = frappe.db.sql(f"""SELECT 
    *
    FROM `tabItem` 
    WHERE item_group='{group}';""", as_dict=True)

    #items = frappe.db.sql("""SELECT * FROM `tabItem`;""", as_dict=True)
    #print(f"\n\n\n{items}\n\n\n")

    if(items):
        status_code = SUCCESS
        body = items
    else:
        status_code = NOT_FOUND
        body = "Items no encontrados"
    response = dict(
        status_code = status_code,
        body = body
    )
    return response
@frappe.whitelist(allow_guest=False)
def add_item(code, name, group, uom):
    add_item = frappe.get_doc({"doctype": "Item",
        "item_code":code,
        "item_name": name,
        "item_group": group,                               
        "stock": uom
                               })
    add_item.insert()
    frappe.db.commit()
    return add_item


@frappe.whitelist(allow_guest=False)
def update_item(code, field, new_value):
    #update_item= frappe.get_all('Item', filters={'name': code}, fields = "*" )
    #update_item = frappe.db.get_value('Item', code, ["*"], as_dict=1)
    #print(update_item.name)
    
    frappe.db.set_value("Item", code, field, new_value)

    #update_item[field] = new_value
    #update_item.save
    frappe.db.commit()
    return "Success"


@frappe.whitelist(allow_guest=False)
def delete_item(name):
    #update_item= frappe.get_all('Item', filters={'name': code}, fields = "*" )
    #update_item = frappe.db.get_value('Item', code, ["*"], as_dict=1)
    #print(update_item.name)
    
    frappe.db.delete("Item", name, {"name": name})

    #update_item[field] = new_value
    #update_item.save
    frappe.db.commit()
    return "deleted"
@frappe.whitelist(allow_guest=False)
def receive_post_data():
    data = json.loads(frappe.request.data)
    doc = frappe.get_doc('Item', data['item_code'])
    client_email = data['client_mail']
    frappe.db.set_value("Item", data['item_code'], "description", f"<div><p>{data['url']}</p></div>")
    
    #frappe.db.commit()
    
    qrcode = pyqrcode.create(data['url'])
    print(f"\n\n\n{data}\n\n\n")
    attachments = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, )]
    #print(qrcode.terminal(quiet_zone=1))
    frappe.sendmail(
        recipients=[client_email],
        subject="Item modificado",
        #template='birthday_reminder',
        message = "Item modificado",
        attachments= attachments
        )
    
    return
