import requests
import subprocess
import sys

def main():
	movie_name = input("Enter the name of the movie\n")
	url = f"https://api.sumanjay.cf/torrent/?query={movie_name}"

	torrent_link = requests.get(url).json()

	index = 1
	magnet= []
	for result in torrent_link:
		print(index, ')',result['name'], result['size'])
		magnet.append(result['magnet'])
		index+=1

	index_choice = int(input("Choose the index of the movie\n"))

	magnet_link = magnet[index_choice-1]

	stream(magnet_link)


def stream(magnet_link):
		cmd=[]
		cmd.append('webtorrent')
		cmd.append(magnet_link)
		cmd.append('--vlc')

		if sys.platform.startswith('linux'):
			subprocess.call(cmd)
		elif sys.platform.startswith('win32'):
			subprocess.call(cmd, shell=True)

main()