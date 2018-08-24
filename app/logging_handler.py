# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""logging handler config"""


def logging_to_email(app):
    """logging email while not debug mode"""
    if app.debug:
        return
    import logging
    from logging.handlers import SMTPHandler
    app_config = app.config
    if app_config["MAIL_SERVER"]:
        auth = None
        if app_config["MAIL_USERNAME"] and app_config["MAIL_PASSWORD"]:
            auth = (app_config["MAIL_USERNAME"], app_config["MAIL_PASSWORD"])
        secure = None
        if app_config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(mailhost=(app_config["MAIL_SERVER"], app_config["MAIL_PORT"]),
                                   fromaddr='no-reply@' + app_config["MAIL_SERVER"],
                                   toaddrs=app_config["ADMINS"],
                                   subject='BSP Failure',
                                   credentials=auth,
                                   secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def logging_to_file(app):
    """logging to file while not debug mode"""
    if app.debug:
        return
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/bsp.log', 'a+', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('bsp startup')


def logging_handler(app):
    """logging handler"""
    if not app.debug:
        logging_to_email(app)
        logging_to_file(app)


__all__ = ['logging_handler']
