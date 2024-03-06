import os
import uuid

from flask import url_for
from main.Authentication.utils import commitDB, saveToDB
from main.Booking.utils import getBookingById
from main.Payment.utils import getPaymentById
from main.Schedule.utils import getScheduleById

from main.Ticket.models import Ticket

from PIL import Image, ImageDraw, ImageFont
import qrcode

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from main.config import Config

def getTicketById(id):
    return Ticket.query.filter_by(id=id).first()

def generate_ticket(tagid, userid, paymentid, scheduleid):
    tagid = tagid
    qrcode = uuid.uuid1().hex
    userid = userid
    paymentid = paymentid
    scheduleid = scheduleid
    newTicket = Ticket(tagid, qrcode, userid, paymentid, scheduleid)
    saveToDB(newTicket)
    # gen ticket image
    generate_ticket_image(newTicket.id)
    return newTicket.tagid

def generate_ticket_image(id):
    ticket = getTicketById(id)
    width, height = 600, 800
    ticket_image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(ticket_image)

    font_path = Config.STATIC_FOLDER_PATH + "/fonts/main.ttf"
    
    print(font_path)
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    scheduleid = ticket.scheduleid
    schedule = getScheduleById(scheduleid)
    movie = schedule.movieref.title 
    date = schedule.start_time.date()
    time = schedule.start_time.time()
    screen = schedule.screenref.name

    paymentid = ticket.paymentid
    payment = getPaymentById(paymentid)
    price = payment.price
    bookingid = payment.booking_id
    booking = getBookingById(bookingid)
    seatid = booking.seatid

    print(movie, date, time, screen, seatid, price)

    qr = qrcode.QRCode(
        box_size=10,
        border=4,
    )
    qr.add_data(ticket.qrcode)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    draw.text((50, 50), f"Movie: {movie}", fill='black', font=font)
    draw.text((50, 100), f"Seat: {seatid}", fill='black', font=font)
    draw.text((50, 150), f"Screen: {screen}", fill='black', font=font)
    draw.text((50, 200), f"Date: {date}", fill='black', font=font)
    draw.text((50, 250), f"Time: {time}", fill='black', font=font)
    draw.text((50, 300), f"Price: {price}", fill='black', font=font)
    ticket_image.paste(qr_image, (50, 340))

    # image_bytes = io.BytesIO()
    # ticket_image.save(image_bytes, format='PNG')
    # image_bytes.seek(0)
    path = Config.STATIC_FOLDER_PATH+Config.TICKET_UPLOAD_PATH
    os.makedirs(path, exist_ok=True)
    image_path = os.path.join(path, f'{ticket.qrcode}.png')
    ticket_image.save(image_path)
    

def create_pdf(image_paths, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    image_width = width / 2
    image_height = height / 2

    x = 0
    y = height - image_height 

    for img_path in image_paths:
        img = Image.open(img_path)

        img.thumbnail((image_width, image_height))

        c.drawImage(img_path, x, y, width=image_width, height=image_height)

        x += image_width

        if x >= width:
            x = 0  
            y -= image_height

            if y < 0:
                c.showPage()
                y = height - image_height  

    c.save()

def getTicketByTagId(tagid):
    return Ticket.query.filter_by(tagid=tagid).all()

def getTicketByUser(userid):
    return Ticket.query.join(Ticket.scheduleref).join(Ticket.paymentref).filter(Ticket.userid==userid).order_by(Ticket.created_at).all()

def getTicketImagePath():
    path = Config.STATIC_FOLDER_PATH+Config.TICKET_UPLOAD_PATH
    return path

def getPdfOutputPath():
    path = Config.STATIC_FOLDER_PATH + Config.PDF_OUTPUT_PATH
    os.makedirs(path, exist_ok=True)
    return path