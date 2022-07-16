from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import refresh_access_token
from twitchAPI.oauth import validate_token
from twitchAPI.types import AuthScope
import lib.scale as scale
import lib.pump as pump
from pprint import pp, pprint
from uuid import UUID
import sys, json, os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/client.json', 'r') as c:
  client = json.load(c)

with open(dir_path + '/tokens.json', 'r') as t:
  tokens = json.load(t)

def user_refresh(token: str, refresh_token: str):
  print(f'my new user token is: {token}')
  tokens['access_token'] = token
  tokens['refresh_token'] = refresh_token
  with open(dir_path + '/tokens.json', 'w') as json_file:
    json.dump(tokens, json_file)

def callback_redemption(uuid: UUID, data: dict) -> None:
  if data['data']['redemption']['reward']['id'] == '657c1a43-bbe1-4710-bcbb-f052d3ea6849':
    # print('got callback for UUID ' + str(uuid))
    # pprint(data)
    scale.init(True)

def init():
  twitch = Twitch(client['clientID'], authenticate_app=False)
  twitch.user_auth_refresh_callback = user_refresh

  if 'status' in validate_token(tokens['access_token']):
    print(validate_token(tokens['access_token'])['status'])
    new_token, new_refresh_token = refresh_access_token(tokens['refresh_token'], client['clientID'], client['clientSecret'])
    tokens['access_token'] = new_token
    tokens['refresh_token'] = new_refresh_token
    with open(dir_path + '/tokens.json', 'w') as json_file:
      json.dump(tokens, json_file)

  # setting up Authentication and getting your user id
  twitch.set_user_authentication(tokens['access_token'], [AuthScope.CHANNEL_READ_REDEMPTIONS], tokens['refresh_token'])

  user_id = twitch.get_users(logins=['Brudehien'])['data'][0]['id']

  # starting up PubSub
  pubsub = PubSub(twitch)
  pubsub.start()
  # you can either start listening before or after you started pubsub.
  uuid = pubsub.listen_channel_points(user_id, callback_redemption)
  input('press ENTER to close...')
  # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
  pubsub.unlisten(uuid)
  pubsub.stop()
  pump.cleanAndExit()