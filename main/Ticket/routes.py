from flask import Blueprint, redirect, render_template, request, send_file, session

from main.Authentication.utils import getUserByUsername, login_required
from main.Ticket.utils import *

ticket = Blueprint("ticket", __name__, template_folder="templates", static_folder="static", static_url_path='/Ticket/static')

# TODO: probably restrict later for unauthorized access
@ticket.route("/<tagid>", methods=['GET', 'POST'])
@login_required
def index(tagid):
    tickets = getTicketByTagId(tagid=tagid)
    if tickets == []:
        return redirect(url_for("home.index"))
    if getUserByUsername(session['user']).id != tickets[0].userid:
        return redirect(url_for("home.index"))
    filename = os.path.join(getPdfOutputPath(), f"{tagid}.pdf")
    if os.path.exists(filename):
        return send_file(filename, download_name='./ticket.pdf')
    ticket_imgs = []
    for ticket in tickets:
        tick = os.path.join(getTicketImagePath(), f'{ticket.qrcode}.png')
        ticket_imgs.append(tick)
    create_pdf(ticket_imgs, filename)
    return send_file(filename, download_name='./ticket.pdf')


@ticket.route("/mytickets/")
@login_required
def mytickets():
    userid = getUserByUsername(session['user']).id
    tickets = getBundledTicketByUser(userid)
    
    return render_template("user_tickets.html",tickets=tickets)