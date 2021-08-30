# -*- coding: utf-8 -*-
"""
Created on Sat May 29 11:17:34 2021

@author: Zetra Team
"""


from flask_detre import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=8100, debug=True, use_reloader=True )

