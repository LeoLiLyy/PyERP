from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations
from app.models import Inventory, db
import hashlib
import os
import requests
import logging
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pathlib import Path
from datetime import date

inventory_bp = Blueprint('inventory', __name__)

logger = logging.getLogger('inventory')


def create_space_chart(used_space, free_space, labels):
    sizes = [used_space, free_space]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode the 1st slice (i.e., 'Used Space')
    mpl.rcParams[u'font.sans-serif'] = ['simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    font = FontProperties(fname='./font/Noto_Sans/static/NotoSans-Regular.ttf')  # Adjust this path as necessary
    plt.figure(figsize=(6, 4))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('app/static/inventory_space.png')  # Ensure the path to save the image is correct
    plt.close()


@inventory_bp.route('/inventory', methods=["GET", "POST"])
@login_required
def inventory():
    items = Inventory.query.all()
    items_in = []
    items_out = []

    for item in items:
        if item.OutDate is None:
            items_in.append(item)
            print(items_in)
        else:
            items_out.append(item)
            print(items_out)

    total_items_in = len(items_in)
    total_capacity = 1000
    used_space = sum(item.Quantity for item in items_in)
    free_space = total_capacity - used_space

    # Get translations for labels
    labels = [g.translations.get('Used Space', 'Used Space'), g.translations.get('Free Space', 'Free Space')]
    create_space_chart(used_space, free_space, labels)

    item_id = request.form.get('item_id')
    action = request.form.get('action')

    if item_id:
        if action == 'i_edit':
            return redirect("/inventory/edit_item/" + str(item_id))
        elif action == 'i_check_out':
            return check_out_item(item_id)
        elif action == 'o_edit':
            return redirect("/inventory/edit_item/" + str(item_id))
        elif action == 'o_del':
            Inventory.query.filter(Inventory.ItemID == item_id).delete()
            db.session.commit()
            return redirect("/inventory/inventory")
        else:
            return redirect("/inventory/inventory")

    return render_template('html/inventory/inventory.html', items=items_in, c_items=items_out,
                           total_items=total_items_in, available_space=free_space)


def check_out_item(item_id):
    today = date.today()
    c_item = Inventory.query.get(item_id)
    c_item.OutDate = today.strftime('%Y-%m-%d')
    db.session.commit()
    logger.info("[*] Checked out item with ID: " + str(item_id))
    return redirect("/inventory/inventory")


@inventory_bp.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    e_item = Inventory.query.get(item_id)
    if request.method == 'POST':
        db.session.add(e_item)
        if request.form.get('name'):
            e_item.I_Name = request.form.get('name')
        if request.form.get('disc'):
            e_item.I_Disc = request.form.get('disc')
        if request.form.get('in_date'):
            e_item.InDate = request.form.get('in_date')
        if request.form.get('warehouse_num'):
            e_item.Warehouse_Num = request.form.get('warehouse_num')
        if request.form.get('quantity'):
            e_item.Quantity = request.form.get('quantity')
        db.session.commit()
        return redirect('/inventory/inventory')
    return render_template('html/inventory/edit_item.html', item=e_item)


@inventory_bp.route('/check_in_item', methods=['GET', 'POST'])
@login_required
def check_in_item():
    if request.method == 'POST':
        today = date.today()
        id = request.form.get('ItemId')
        name = request.form.get('i_name')
        disc = request.form.get('i_disc')
        i_date = today.strftime('%Y-%m-%d')
        od = None
        warehouse_num = request.form.get('warehouse_num')
        quantity = request.form.get('quantity')
        new_item = Inventory(ItemID=id, I_Name=name, I_Disc=disc, InDate=i_date, OutDate=od,
                             Warehouse_Num=warehouse_num,
                             Quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/inventory/inventory')  # Redirect to inventory page
    return render_template('/html/inventory/item_in.html')
