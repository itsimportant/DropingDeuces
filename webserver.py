import socket
import tweepy
import random
import time

HOST, PORT = '', 8888

def get_tweet():
	txt = open("/home/pi/Programs/BathroomTweet/tweets.txt")
	line = txt.readlines()
	num = random.randint(0, 300)
	tweet = line[num].strip()+" #ToiletTweets #MrDooky"
	return tweet

def get_api(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)

def poop(msg):
	cfg = {
	"consumer_key"		:"****",
	"consumer_secret"	:"****",
	"access_token"		:"****",
	"access_token_secret"	:"****",
	}
	
	api = get_api(cfg)
	status = api.update_status(status=msg)
	return

def main():
	prevPoop = 0
	
	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listen_socket.bind((HOST, PORT))
	listen_socket.listen(1)

	print 'Server started on port %s. ' % PORT
	while True:
		client_connection, client_address = listen_socket.accept()
		request = client_connection.recv(1024)
		http_response  = """HTTP/1.1 302 OK
Location: http://10.0.0.106/pooped.html
""" 
		currentPoop = time.time()
		if (currentPoop - prevPoop) > 600:
			tweet = get_tweet()
			poop(tweet)
			prevPoop = currentPoop
		client_connection.sendall(http_response)
		client_connection.close()

main()
