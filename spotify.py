from dotenv import load_dotenv
import os
import base64
from requests import post
import secrets
import hashlib
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-read-currently-playing, user-modify-playback-state"

"""
Generating PKCE verifier + challenge
"""

def generate_code_verifier():
  return secrets.token_urlsafe(64)

def generate_code_challenge(verifier):
  digest = hashlib.sha256(verifier.encode()).digest()
  encoded_string = base64.urlsafe_b64encode(digest)
  converted_string = encoded_string.decode()
  clean_string = converted_string.rstrip("=")

  return clean_string

"""
Get authorization code from spotify
"""

def get_authorization_code():
  code_verifier = generate_code_verifier()
  code_challenge = generate_code_challenge(code_verifier)
  state = secrets.token_urlsafe(16)

  params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "code_challenge_method": "S256",
    "code_challenge": code_challenge,
    "scope": SCOPE,
    "state": state,
  }

  authorization_url = (
    "https://accounts.spotify.com/authorize?" + urlencode(params)
  )
  authorization_code = None

  class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      nonlocal authorization_code
      query = parse_qs(urlparse(self.path).query)

      returned_state = query.get("state", [None])[0]
      if returned_state != state:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"State mismatch")
        return

      authorization_code = query.get("code", [None])[0]
      self.send_response(200)
      self.end_headers()
      message = r"""
        @ @ @ # # #
     # # @ @ @ @ # # #
    S @ @ @ @ @ @ @ @ @ @ @
    @ @ @ @ @ @ @ @ @ @ @ @ @ S # % % % @
   S # @ @ @ @ @ @  @ @ @ @ # S S S ? * + @
   S # @ @ @ @ @      + ? # @ # # S % % + +
   S # @ @ @ @ @     : : : : , ? S # # # # ? * * * *
    # @ @ @ @ @    + ; + + + + ; : : * ? S S # % * * * S
    S # @ @ @    * + * * ? % % % S # + : ; : S S S ? * * +
      # @     * + * % S S # S S % ? S S + ; + S % * * * ?
            * * + * ? % S # @ @ # + * S S % ; + ? ? ? ? ? ?
           # S % % % % % S # @ @ @ # , % S S ? + * ? ? % S S
           # S # # # @ @ @ @ @ @ @ @ , ; S S % S % * + ? % ? ?
               @ @ @ @ @ @ @ @ @ ? , S S % S ? ? * * * * ; ;
                # @ @ @ @ @ @ @ S , # S % ? % ? % ? ? * + * *
                 @ @ @ @ @ @ @ S , # * S ? * * + * ? ? ? ? ?
                  @ @ @ @ @ @ ; , # % + + * * + % * ? % * * ?
                   @ @ @ # ; , S S ? ; ? ? + * % % * S * + + *
                     # ? : * ; : ? * ; ? S ? % % + * ? : * ? * * +
                    ; , + * * ? ? ? ? * + + * + ? + ; * ? + + * * * * * *
                    ; + + + ? * ? ; + + + + * + + + ; * ? * * + + * * * * * *
                    + + + ? * ? + ; * ? ? * + + + + + * + * * * * * * * * * * * ? *
                   : + + + + + ; * + + + * + * * + * + * * * * * * * * * * * * * * * + ? *
                   ; + + + + * + * + * * * * + + * * * * * * * * * * * * * * * + + * * ? ? ?
                   + + + + + * + * + + + * * * * * * + + * * * * * * * * * * * * * + * * * * * ? ? ?
                   * + + + + * * + * + + * * * * * * + + * * * * * * * * * * * * * * * * * + * * * * * * ?
                   + + + + * + * * * * * * * * + : : ; ; + ? * * * * * * * * * * + * * * * * * * * + * * * * * %
                   * + + + + * * * * * * * * * * + + : : + * * * * + * * * * * * * * * * * * + + + * * * + * * ? *
                   * + + + * * * * * * * ? * * * * * + ; : + + + ; * ? ? * * * * * * * * * * * * * ; ; * * * * * * + @
                   * * * * * * * * * * * ? ? ? ? ? ? ? ? ? ? ? ? + ; * % ? ? ? * * * * * * * * * * * * + + * * * + * * *
                    ? * * + * * ? * ? ? ? ? ? ? ? ? ? % ? ? ? ? ? ? ? ? ? ? ? ? ? ? * * * * * * * * ? * ; + * * * * * * * * ?
                    % ? * * * * ? ? ? ? * ; : ; * ? ? ? ? ? ? ? ? ? * : , , : ; * * * ? ? * * ? ? * ? ? * : + * * * * * * * ? %
                     * * * * * ? ? ? ? % % ? * : , ; * : : ? ? : + ? * * ? % % ? * ? * * * ? ? ? ? ? ? ? ? + + * * * * * * ? ? * :
                     % * * * * ? ? ? % % % % % ? * * ? % % % % % ? % ? ? ? ? * * * ? * ? ? ? ? ? ? ? ? ? ? * + + * * * * * * * * * ?
                      ? ? * ? ? ? ? ? ? % % % % % % % % % % ? ? % ? ? ? ? * ; : ; ; + + * * + * ? ? ? ? ? ? ? ; * + * * * * * * * ? %
                      ? ? ? ? ? % % ? * ? % % % % % % * * + + * ? + ? ? ? * * ? % * + ; ; ; ; + ? ? ? ? ? ? ? ? ? ; + + * * * * * ? % S
                       ? ? + ? % % % ? * + + * ? * ? * + + * % ? + ? % % % % % % % % ? * * ? * + + + + * ? ? ? ? ? + + + * * * * * ? % %
                       ? ? + ? ? % % % % * * * % + + S S S % % % % ? + + + + ? % + * ? * ? % ? * * * * ? * ? ? ? ? ? ? + + + * * * * ? ? %
                        % + ? % % % % % % S % S S ? S % % % % % % % ? * * * % % ? ? % % % S % % % % % ? ? * ? ? ? ? ? ? * + + + * * * * *
                         * + * % S % % % % S % * S S S % S S S S S S S S S S S S S S S S S S % % % ? ? ? ? ? * * ? ? ? ? ? * + + + * * * %
                         + * ? ? % ? ? % % + * * ; ; % + * * + ? % ? * % S S S S S S + : : + % S % % % % * ? ? * * ? ? ? ? ? ? * * * * + * +
                          ? ? ? S S S % ? % ? S % % # S S % ? % S S S S * ; : * ; ? S S S S S * ; : : : ; * + + * + + + * ? ? ? ? ? * * + + ?
                          * ? ? ? ? S * ? S ? S * # + S S S # S S ? + + ? S S S # # # # # # # # S S S S S S S S % % * + ? S % ? * * * * * * * ?
                            # % * * * * + * # S @ @ S + * # % % # # # # S # # S S # # S S S S S S S # # ? % % + * + ; : + ? ? * * * * * * * * % %
                            + ? % S ? % S S * # * ? # % # # S % S # S S + ; + S * ? % ? * * ? * + + ; ; ; + + ; + % S % + ; * ? * * * * * + * * * + .
                             ? % S % S * % # # % S @ S # ? ? S S % ? S # # S % % % % * + * * + + * % ? % % % % ? ? % % % % ? ? * * * * * * * * + + * + +
                              * * ? S % # * @ ? ? # S S # S S # S % % S # * + + + ? S % * ? % S S S % S S # # % % % % ? * * * * * * * * * * * * * * + + + ;
                               ? S % # S ? # @ S # ? % S * * % % % S S # S S S % % S % % # # % * ? ? % S S S % S S S % ? * * * * * * * * + * * * * + + + + + ;
                                @ # S ? % S @ ? @ S # # * + ? % ? * S # % % % ? ? S S ? % % % % S @ S S % % % % S S % % % S ? ? % * * ? + * * * * * * * + + + ;
                                  * % S S # S S S # # % S # # ? % # # # @ % % S # S % % % % S # S % % % S # S S % S S S S # S S % % % ? ? * * + * * * * * + +
                                    % # # # S # % @ # @ @ # % # @ # % S % % % % S S % S % % % % % S # # # # S S S # # S # S S % % % % % ? ? * + * + * * + *
                                      # # # # # @ # S # @ S % # @ S S # S % % % % % % ? % S # # # # # # # S S S S S S S S S % % S # % % % % ? ? * + + + +
                                       @ # # # S @ # @ @ S S @ @ S # S # S # # # # S # # S # # S S # #       % S S ? @ @ # S % % % % % ? ? * + +
                                         S S S # # @ @ # @ @ # S # # # S S S # # # # # S ? % S %                    ? % % % * + *
                                           @ # # # # # @ @ # # # @ @ # # # @ @ # # S S % + :
                                             @ @ # # # S # # # # # S @ @ @ @ @ @  ? ? ? % ,
                                                 @ S # S S S S %        ? * ; ,
                                                  % S S % S % %        ? ? * ,
                                                   % % ? % S S        ? ? * ,
                                                   ? ? % % %         ? ? ? % ,
                                                   * ? ? ? S         ? ? ? ? ,
                                                   * ? ? %          ? * ? * ,
                                                  + * * ?           % * ? ,
                                                  * * * %           ? ? % ,
                                                 + * * *            ? % S ,
                                                 + + * *            + % S ,
                                                + * * * .            * ? ,
                                                + + + ;               + - 
                                             ______())             ____())                        
      """
      self.wfile.write(message.encode("utf-8"))

    def log_message(self,format,*args):
      pass

  print("Opening Spotify authorization page...")
  webbrowser.open(authorization_url)
  server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)

  while authorization_code is None:
    server.handle_request()

  server.server_close()
  return authorization_code, code_verifier

"""
Exchange authorization code for tokens
"""

def exchange_code_for_token(authorization_code, code_verifier):
  url = "https://accounts.spotify.com/api/token"
  data = {
    "client_id": CLIENT_ID,
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": REDIRECT_URI,
    "code_verifier": code_verifier,
    }
  response = post(url, data=data, headers={"Content-Type":"application/x-www-form-urlencoded"})
  response.raise_for_status()
  return response.json()

def get_auth_header(token):
  return {"Authorization": "Bearer " + token}

def get_tokens():
  code, verifier = get_authorization_code()
  tokens = exchange_code_for_token(code, verifier)
  return tokens["access_token"], tokens["refresh_token"]

def get_new_token(refresh_token):
  url = "https://accounts.spotify.com/api/token"
  data = {
    "client_id": CLIENT_ID,
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
  }
  header = {
    "Content-Type":"application/x-www-form-urlencoded"
  }
  response = post(url,data=data,headers=header)
  response.raise_for_status()
  response.json()
  return response["access_token"]