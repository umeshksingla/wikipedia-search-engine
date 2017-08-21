import sys

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: bash index.sh <path-to-wiki-dump> <path-to-invertedindex (outputfile)>"
		sys.exit(1)

		