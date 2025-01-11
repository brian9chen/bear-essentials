from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request

class CartItem:
    def __init__(self, word, discount):
        self.id = id
        self.word = word
        self.discount = discount
