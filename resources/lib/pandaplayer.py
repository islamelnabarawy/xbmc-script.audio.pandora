from threading import Timer
import xbmc
import xbmcaddon
import os, sys

##_settings   = xbmcaddon.Addon()
##_name       = _settings.getAddonInfo('name')
##_version    = _settings.getAddonInfo('version')
##_path       = xbmc.translatePath( _settings.getAddonInfo('path') ).decode('utf-8')
##_lib        = xbmc.translatePath( os.path.join( _path, 'resources', 'lib' ) )

##sys.path.append (_lib)

from utils import *

##_NAME = _name.upper()

class PandaPlayer( xbmc.Player ):

	class ScreensaverExitMonitor( xbmc.Monitor ):
		# URLref: [script.screensaver.test] https://github.com/dersphere/script.screensaver.test/blob/master/default.py
		##def __init__(self, exit_callback):
		##    self.exit_callback = exit_callback
		def __init__ ( self ):
			pass

		def onScreensaverDeactivated(self):
			##print '3 ExitMonitor: sending exit_callback'
			##self.exit_callback()
			# show UI
			xbmc.executebuiltin('Skin.Reset(PandoraVis)')

	##def do_exitScreensaver(self):
	##    print '4 Screensaver: Exit requested'
	##    self.close()

	def __init__( self, core=None, panda=None ):
		xbmc.Player.__init__( self )
		self.panda = panda
		self.timer = None
		self.playNextSong_delay = 0.5
		self.monitor = self.ScreensaverExitMonitor()

	def playSong( self, item ):
		log.debug( "playSong: item[url] %s" % item[0] )
		log.debug( "playSong: item[item] %s" % item[1] )
		self.play( item[0], item[1] )

	def play( self, url, item ):
		# override play() to force use of PLAYER_CORE_MPLAYER
		xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play( url, item )

		# NOTE: using PLAYER_CORE_MPLAYER is necessary to play .mp4 streams (low & medium quality from Pandora)
		#   ... unfortunately, using "xbmc.Player([core]) is deprecated [ see URLref: http://forum.xbmc.org/showthread.php?tid=173887&pid=1516662#pid1516662 ]
		#   ... and it may be removed from Gotham [ see URLref: https://github.com/xbmc/xbmc/pull/1427 ]
		# ToDO: discuss with the XBMC Team what the solution to this problem would be

	def onPlayBackStarted( self ):
		log.debug( "onPlayBackStarted: %s" %self.getPlayingFile() )
		if self.panda.playing:
			pass
			### ToDO: ? remove checks for pandora.com / p-cdn.com (are they needed? could be a maintainence headache if the cdn changes...)
			##if not "pandora.com" in self.getPlayingFile():
			##	if not "p-cdn.com" in self.getPlayingFile():
			##		self.panda.playing = False
			##		self.panda.quit()
			##else:
				# show visualization (o/w disappears when song is started...)
				##xbmc.executebuiltin( "ActivateWindow( 12006 )" )
				##xbmc.executebuiltin( "ActivateWindow( 12900 )" )

	def onPlayBackEnded( self ):
		log.debug( "onPlayBackEnded" )
		self.stop()
		log.debug( "playing = %s" %self.panda.playing )
		if self.timer and self.timer.isAlive():
			self.timer.cancel()
		if self.panda.skip:
			self.panda.skip = False
		if self.panda.playing:
			self.timer = Timer( self.playNextSong_delay, self.panda.playNextSong )
			self.timer.start()

	def onPlayBackStopped( self ):
		log.debug( "onPlayBackStopped" )
		self.stop()
		log.debug( "playing = %s" %self.panda.playing )
		if self.timer and self.timer.isAlive():
			self.timer.cancel()
		if self.panda.playing and self.panda.skip:
			self.panda.skip = False
			self.timer = Timer( self.playNextSong_delay, self.panda.playNextSong )
			self.timer.start()
		else:
			if xbmc.getCondVisibility('Skin.HasSetting(PandoraVis)'):
				# show UI
				xbmc.executebuiltin('Skin.Reset(PandoraVis)')
			self.panda.stop()
