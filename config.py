import os

class Config:
  __conf = {
    "save_media_to": os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "${Y}" + os.path.sep + "${m}" + os.path.sep + "${F}T${t}_${N}_${SN}",
    "tfa_type": "PUSH",
    "tfa_source": "push",
    "tfa_retries": 10,
    "tfa_delay": 5,
    "tfa_host": '',
    "tfa_username": '',
    "tfa_password": ''
  }
  __setters = [
    "set_logger",
    "save_media_to",
    "tfa_type",
    "tfa_source",
    "tfa_retries",
    "tfa_delay",
    "tfa_host",
    "tfa_username",
    "tfa_password"
    ]
  @staticmethod
  def config(name):
    return Config.__conf[name]

  def dump_config():
    return Config.__conf

  @staticmethod
  def set(name, value):
    if name in Config.__setters:
      Config.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")
