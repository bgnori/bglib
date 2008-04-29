#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re

'''
  FIBS_UNINITIALIZED_STATE,
  FIBS_LOGIN_STATE,
  FIBS_MOTD_STATE,
  FIBS_RUN_STATE,
  FIBS_LOGOUT_STATE
'''
  
class Monster(object):
  pass


class CookieDough(object):
  def __iter__(self):
    pass

class AlphaBatch(CookieDough):
  FIBS_Board = "^board:[a-zA-Z_<>]+:[a-zA-Z_<>]+:[0-9:\\-]+$"
  FIBS_BAD_Board = "^board:"
  FIBS_YouRoll = "^You roll [1-6] and [1-6]"
  FIBS_PlayerRolls = "^[a-zA-Z_<>]+ rolls [1-6] and [1-6]"
  FIBS_RollOrDouble = "^It's your turn to roll or double\\."
  FIBS_RollOrDouble = "^It's your turn\\. Please roll or double"
  FIBS_AcceptRejectDouble = "doubles\\. Type 'accept' or 'reject'\\."
  FIBS_Doubles = "^[a-zA-Z_<>]+ doubles\\."
  FIBS_PlayerAcceptsDouble = "accepts the double\\."
  FIBS_PleaseMove = "^Please move [1-4] pieces?\\."
  FIBS_PlayerMoves = "^[a-zA-Z_<>]+ moves"
  FIBS_BearingOff = "^Bearing off:"
  FIBS_YouReject = "^You reject\\. The game continues\\."
  FIBS_YouStopWatching = "You're not watching anymore\\." # overloaded  //PLAYER logs out.. You're not watching anymore.
  FIBS_OpponentLogsOut = "The game was saved\\." # PLAYER logs out. The game was saved. ||  PLAYER drops connection. The game was saved.
  FIBS_OnlyPossibleMove = "^The only possible move is"
  FIBS_FirstRoll = "[a-zA-Z_<>]+ rolled [1-6].+rolled [1-6]"
  FIBS_MakesFirstMove = " makes the first move\\."
  FIBS_YouDouble = "^You double\\. Please wait for " # You double. Please wait for PLAYER to accept or reject.
  FIBS_PlayerWantsToResign = "^[a-zA-Z_<>]+ wants to resign\\. You will win [0-9]+ points?\\. Type 'accept' or 'reject'\\."
  FIBS_WatchResign = "^[a-zA-Z_<>]+ wants to resign\\. " # PLAYER wants to resign. PLAYER2 will win 2 points.  (ORDER MATTERS HERE)
  FIBS_YouResign = "^You want to resign\\." # You want to resign. PLAYER will win 1 .
  FIBS_ResumeMatchAck5 = "^You are now playing with [a-zA-Z_<>]+\\. Your running match was loaded\\."
  FIBS_JoinNextGame = "^Type 'join' if you want to play the next game, type 'leave' if you don't\\."
  FIBS_NewMatchRequest = "^[a-zA-Z_<>]+ wants to play a [0-9]+ point match with you\\."
  FIBS_WARNINGSavedMatch = "^WARNING: Don't accept if you want to continue"
  FIBS_ResignRefused = "rejects\\. The game continues\\."
  FIBS_MatchLength = "^match length:"
  FIBS_TypeJoin = "^Type 'join [a-zA-Z_<>]+' to accept\\."
  FIBS_YouAreWatching = "^You're now watching "
  FIBS_YouStopWatching = "^You stop watching " # overloaded
  FIBS_PlayerStartsWatching = "[a-zA-Z_<>]+ starts watching [a-zA-Z_<>]+\\."
  FIBS_PlayerStartsWatching = "[a-zA-Z_<>]+ is watching you\\."
  FIBS_PlayerStopsWatching = "[a-zA-Z_<>]+ stops watching [a-zA-Z_<>]+\\."
  FIBS_PlayerIsWatching = "[a-zA-Z_<>]+ is watching "
  FIBS_ResignWins = "^[a-zA-Z_<>]+ gives up\\. [a-zA-Z_<>]+ wins [0-9]+ points?\\." # PLAYER1 gives up. PLAYER2 wins 1 point.
  FIBS_ResignYouWin = "^[a-zA-Z_<>]+ gives up\\. You win [0-9]+ points?\\."
  FIBS_YouAcceptAndWin = "^You accept and win"
  FIBS_AcceptWins = "^[a-zA-Z_<>]+ accepts and wins [0-9]+ point" # PLAYER accepts and wins N points.
  FIBS_PlayersStartingMatch = "^[a-zA-Z_<>]+ and [a-zA-Z_<>]+ start a [0-9]+ point match" # PLAYER and PLAYER start a <n> point match.
  FIBS_StartingNewGame = "^Starting a new game with "
  FIBS_YouGiveUp = "^You give up\\. "
  FIBS_YouWinMatch = "^You win the [0-9]+ point match"
  FIBS_PlayerWinsMatch = "^[a-zA-Z_<>]+ wins the [0-9]+ point match" #PLAYER wins the 3 point match 3-0 .
  FIBS_ResumingUnlimitedMatch = "^[a-zA-Z_<>]+ and [a-zA-Z_<>]+ are resuming their unlimited match\\."
  FIBS_ResumingLimitedMatch = "^[a-zA-Z_<>]+ and [a-zA-Z_<>]+ are resuming their [0-9]+-point match\\."
  FIBS_MatchResult = "^[a-zA-Z_<>]+ wins a [0-9]+ point match against " #PLAYER wins a 9 point match against PLAYER  11-6 .
  FIBS_PlayerWantsToResign = "wants to resign\\." #  Same as a longline in an actual game  This is just for watching.

  FIBS_BAD_AcceptDouble = "^[a-zA-Z_<>]+ accepts? the double\\. The cube shows [0-9]+\\..+"
  FIBS_YouAcceptDouble = "^You accept the double\\. The cube shows"
  FIBS_PlayerAcceptsDouble = "^[a-zA-Z_<>]+ accepts the double\\. The cube shows "
  FIBS_PlayerAcceptsDouble = "^[a-zA-Z_<>]+ accepts the double\\." # while watching
  FIBS_ResumeMatchRequest = "^[a-zA-Z_<>]+ wants to resume a saved match with you\\."
  FIBS_ResumeMatchAck0 = "has joined you\\. Your running match was loaded"
  FIBS_YouWinGame = "^You win the game and get"
  FIBS_UnlimitedInvite = "^[a-zA-Z_<>]+ wants to play an unlimted match with you\\."
  FIBS_PlayerWinsGame = "^[a-zA-Z_<>]+ wins the game and gets [0-9]+ points?. Sorry."
  FIBS_PlayerWinsGame = "^[a-zA-Z_<>]+ wins the game and gets [0-9]+ points?." # (when watching)
  FIBS_WatchGameWins = "wins the game and gets"
  FIBS_PlayersStartingUnlimitedMatch = "start an unlimited match\\." # PLAYER_A and PLAYER_B start an unlimited match.
  FIBS_ReportLimitedMatch = "^[a-zA-Z_<>]+ +- +[a-zA-Z_<>]+ .+ point match" # PLAYER_A        -       PLAYER_B (5 point match 2-2)
  FIBS_ReportUnlimitedMatch = "^[a-zA-Z_<>]+ +- +[a-zA-Z_<>]+ \\(unlimited"
  FIBS_ShowMovesStart = "^[a-zA-Z_<>]+ is X - [a-zA-Z_<>]+ is O"
  FIBS_ShowMovesRoll = "^[XO]: \\([1-6]" # ORDER MATTERS HERE
  FIBS_ShowMovesWins = "^[XO]: wins"
  FIBS_ShowMovesDoubles = "^[XO]: doubles"
  FIBS_ShowMovesAccepts = "^[XO]: accepts"
  FIBS_ShowMovesRejects = "^[XO]: rejects"
  FIBS_ShowMovesOther = "^[XO]:" # AND HERE
  FIBS_ScoreUpdate = "^score in [0-9]+ point match:"
  FIBS_MatchStart = "^Score is [0-9]+-[0-9]+ in a [0-9]+ point match\\."
  FIBS_Settings = "^Settings of variables:"
  FIBS_Turn = "^turn:"
  FIBS_Boardstyle = "^boardstyle:"
  FIBS_Linelength = "^linelength:"
  FIBS_Pagelength = "^pagelength:"
  FIBS_Redoubles = "^redoubles:"
  FIBS_Sortwho = "^sortwho:"
  FIBS_Timezone = "^timezone:"
  FIBS_CantMove = "^[a-zA-Z_<>]+ can't move" # PLAYER can't move || You can't move
  FIBS_ListOfGames = "^List of games:"
  FIBS_PlayerInfoStart = "^Information about"
  FIBS_EmailAddress = "^  Email address:"
  FIBS_NoEmail = "^  No email address\\."
  FIBS_WavesAgain = "^[a-zA-Z_<>]+ waves goodbye again\\."
  FIBS_Waves = "waves goodbye"
  FIBS_Waves = "^You wave goodbye\\."
  FIBS_WavesAgain = "^You wave goodbye again and log out\\."
  FIBS_NoSavedGames = "^no saved games\\."
  FIBS_TypeBack = "^You're away\\. Please type 'back'"
  FIBS_SavedMatch = "^  [a-zA-Z_<>]+ +[0-9]+ +[0-9]+ +- +"
  FIBS_SavedMatchPlaying = "^ \\*[a-zA-Z_<>]+ +[0-9]+ +[0-9]+ +- +"
  #  NOTE: for FIBS_SavedMatchReady, see the Stars message, because it will appear to be one of those (has asterisk at index 0).
  FIBS_PlayerIsWaitingForYou = "^[a-zA-Z_<>]+ is waiting for you to log in\\."
  FIBS_IsAway = "^[a-zA-Z_<>]+ is away: "
  FIBS_AllowpipTrue = "^allowpip +YES"
  FIBS_AllowpipFalse = "^allowpip +NO"
  FIBS_AutoboardTrue = "^autoboard +YES"
  FIBS_AutoboardFalse = "^autoboard +NO"
  FIBS_AutodoubleTrue = "^autodouble +YES"
  FIBS_AutodoubleFalse = "^autodouble +NO"
  FIBS_AutomoveTrue = "^automove +YES"
  FIBS_AutomoveFalse = "^automove +NO"
  FIBS_BellTrue = "^bell +YES"
  FIBS_BellFalse = "^bell +NO"
  FIBS_CrawfordTrue = "^crawford +YES"
  FIBS_CrawfordFalse = "^crawford +NO"
  FIBS_DoubleTrue = "^double +YES"
  FIBS_DoubleFalse = "^double +NO"
  FIBS_MoreboardsTrue = "^moreboards +YES"
  FIBS_MoreboardsFalse = "^moreboards +NO"
  FIBS_MovesTrue = "^moves +YES"
  FIBS_MovesFalse = "^moves +NO"
  FIBS_GreedyTrue = "^greedy +YES"
  FIBS_GreedyFalse = "^greedy +NO"
  FIBS_NotifyTrue = "^notify +YES"
  FIBS_NotifyFalse = "^notify +NO"
  FIBS_RatingsTrue = "^ratings +YES"
  FIBS_RatingsFalse = "^ratings +NO"
  FIBS_ReadyTrue = "^ready +YES"
  FIBS_ReadyFalse = "^ready +NO"
  FIBS_ReportTrue = "^report +YES"
  FIBS_ReportFalse = "^report +NO"
  FIBS_SilentTrue = "^silent +YES"
  FIBS_SilentFalse = "^silent +NO"
  FIBS_TelnetTrue = "^telnet +YES"
  FIBS_TelnetFalse = "^telnet +NO"
  FIBS_WrapTrue = "^wrap +YES"
  FIBS_WrapFalse = "^wrap +NO"
  FIBS_Junk = "^Closed old connection with user"
  FIBS_Done = "^Done\\."
  FIBS_YourTurnToMove = "^It's your turn to move\\."
  FIBS_SavedMatchesHeader = "^  opponent          matchlength   score \\(your points first\\)"
  FIBS_MessagesForYou = "^There are messages for you:"
  FIBS_RedoublesSetTo = "^Value of 'redoubles' set to [0-9]+\\."
  FIBS_DoublingCubeNow = "^The number on the doubling cube is now [0-9]+"
  FIBS_FailedLogin = "^> [0-9]+" # bogus CLIP messages sent after a failed login
  FIBS_Average = "^Time (UTC)  average min max"
  FIBS_DiceTest = "^[nST]: "
  FIBS_LastLogout = "^  Last logout:"
  FIBS_RatingCalcStart = "^rating calculation:"
  FIBS_RatingCalcInfo = "^Probability that underdog wins:"
  FIBS_RatingCalcInfo = "is 1-Pu if underdog wins" # P=0.505861 is 1-Pu if underdog wins and Pu if favorite wins
  FIBS_RatingCalcInfo = "^Experience: " # Experience: fergy 500 - jfk 5832
  FIBS_RatingCalcInfo = "^K=max\\(1" # K=max(1 ,    -Experience/100+5) for fergy: 1.000000
  FIBS_RatingCalcInfo = "^rating difference"
  FIBS_RatingCalcInfo = "^change for" # change for fergy: 4*K*sqrt(N)*P=2.023443
  FIBS_RatingCalcInfo = "^match length  "
  FIBS_WatchingHeader = "^Watching players:"
  FIBS_SettingsHeader = "^The current settings are:"
  FIBS_AwayListHeader = "^The following users are away:"
  FIBS_RatingExperience = "^  Rating: +[0-9]+\\." # Rating: 1693.11 Experience: 5781
  FIBS_NotLoggedIn = "^  Not logged in right now\\."
  FIBS_IsPlayingWith = "is playing with"
  FIBS_SavedScoreHeader = "^opponent +matchlength" #  opponent          matchlength   score (your points first)
  FIBS_StillLoggedIn = "^  Still logged in\\." #  Still logged in. 2:12 minutes idle.
  FIBS_NoOneIsAway = "^None of the users is away\\."
  FIBS_PlayerListHeader = "^No  S  username        rating  exp login    idle  from"
  FIBS_RatingsHeader = "^ rank name            rating    Experience"
  FIBS_ClearScreen = "^.\\[;H.\\[2J" # ANSI clear screen sequence
  FIBS_Timeout = "^Connection timed out\\."
  FIBS_Goodbye = "           Goodbye\\."
  FIBS_LastLogin = "^  Last login:"
  FIBS_NoInfo = "^No information found on user"

class NumericBatch(CookieDough):
  CLIP_WHO_INFO = "^5 [^ ]+ - - [01]"
  CLIP_WHO_INFO = "^5 [^ ]+ [^ ]+ - [01]"
  CLIP_WHO_INFO = "^5 [^ ]+ - [^ ]+ [01]"

  FIBS_Average = "^[0-9][0-9]:[0-9][0-9]-" # output of average command
  FIBS_DiceTest = "^[1-6]-1 [0-9]" # output of dicetest command
  FIBS_DiceTest = "^[1-6]: [0-9]"
  FIBS_Stat = "^[0-9]+ bytes" # output from stat command
  FIBS_Stat = "^[0-9]+ accounts"
  FIBS_Stat = "^[0-9]+ ratings saved. reset log"
  FIBS_Stat = "^[0-9]+ registered users."
  FIBS_Stat = "^[0-9]+\\([0-9]+\\) saved games check by cron"

  CLIP_WHO_END = "^6$"
  CLIP_SHOUTS = "^13 [a-zA-Z_<>]+ "
  CLIP_SAYS = "^12 [a-zA-Z_<>]+ "
  CLIP_WHISPERS = "^14 [a-zA-Z_<>]+ "
  CLIP_KIBITZES = "^15 [a-zA-Z_<>]+ "
  CLIP_YOU_SAY = "^16 [a-zA-Z_<>]+ "
  CLIP_YOU_SHOUT = "^17 "
  CLIP_YOU_WHISPER = "^18 "
  CLIP_YOU_KIBITZ = "^19 "
  CLIP_LOGIN = "^7 [a-zA-Z_<>]+ "
  CLIP_LOGOUT = "^8 [a-zA-Z_<>]+ "
  CLIP_MESSAGE = "^9 [a-zA-Z_<>]+ [0-9]+ "
  CLIP_MESSAGE_DELIVERED = "^10 [a-zA-Z_<>]+$"
  CLIP_MESSAGE_SAVED = "^11 [a-zA-Z_<>]+$"


class StarsBatch(CookieDough):
  FIBS_Username = "^\\*\\* User"
  FIBS_Junk = "^\\*\\* You tell " # "** You tell PLAYER: xxxxx"
  FIBS_YouGag = "^\\*\\* You gag"
  FIBS_YouUngag = "^\\*\\* You ungag"
  FIBS_YouBlind = "^\\*\\* You blind"
  FIBS_YouUnblind = "^\\*\\* You unblind"
  FIBS_UseToggleReady = "^\\*\\* Use 'toggle ready' first"
  FIBS_NewMatchAck9 = "^\\*\\* You are now playing an unlimited match with "
  FIBS_NewMatchAck10 = "^\\*\\* You are now playing a [0-9]+ point match with " # ** You are now playing a 5 point match with PLAYER
  FIBS_NewMatchAck2 = "^\\*\\* Player [a-zA-Z_<>]+ has joined you for a" # ** Player PLAYER has joined you for a 2 point match.
  FIBS_YouTerminated = "^\\*\\* You terminated the game"
  FIBS_OpponentLeftGame = "^\\*\\* Player [a-zA-Z_<>]+ has left the game. The game was saved\\."
  FIBS_PlayerLeftGame = "has left the game\\." # overloaded
  FIBS_YouInvited = "^\\*\\* You invited"
  FIBS_YourLastLogin = "^\\*\\* Last login:"
  FIBS_NoOne = "^\\*\\* There is no one called"
  FIBS_AllowpipFalse = "^\\*\\* You don't allow the use of the server's 'pip' command\\."
  FIBS_AllowpipTrue = "^\\*\\* You allow the use the server's 'pip' command\\."
  FIBS_AutoboardFalse = "^\\*\\* The board won't be refreshed"
  FIBS_AutoboardTrue = "^\\*\\* The board will be refreshed"
  FIBS_AutodoubleTrue = "^\\*\\* You agree that doublets"
  FIBS_AutodoubleFalse = "^\\*\\* You don't agree that doublets"
  FIBS_AutomoveFalse = "^\\*\\* Forced moves won't"
  FIBS_AutomoveTrue = "^\\*\\* Forced moves will"
  FIBS_BellFalse = "^\\*\\* Your terminal won't ring"
  FIBS_BellTrue = "^\\*\\* Your terminal will ring"
  FIBS_CrawfordFalse = "^\\*\\* You would like to play without using the Crawford rule\\."
  FIBS_CrawfordTrue = "^\\*\\* You insist on playing with the Crawford rule\\."
  FIBS_DoubleFalse = "^\\*\\* You won't be asked if you want to double\\."
  FIBS_DoubleTrue = "^\\*\\* You will be asked if you want to double\\."
  FIBS_GreedyTrue = "^\\*\\* Will use automatic greedy bearoffs\\."
  FIBS_GreedyFalse = "^\\*\\* Won't use automatic greedy bearoffs\\."
  FIBS_MoreboardsTrue = "^\\*\\* Will send rawboards after rolling\\."
  FIBS_MoreboardsFalse = "^\\*\\* Won't send rawboards after rolling\\."
  FIBS_MovesTrue = "^\\*\\* You want a list of moves after this game\\."
  FIBS_MovesFalse = "^\\*\\* You won't see a list of moves after this game\\."
  FIBS_NotifyFalse = "^\\*\\* You won't be notified"
  FIBS_NotifyTrue = "^\\*\\* You'll be notified"
  FIBS_RatingsTrue = "^\\*\\* You'll see how the rating changes are calculated\\."
  FIBS_RatingsFalse = "^\\*\\* You won't see how the rating changes are calculated\\."
  FIBS_ReadyTrue = "^\\*\\* You're now ready to invite or join someone\\."
  FIBS_ReadyFalse = "^\\*\\* You're now refusing to play with someone\\."
  FIBS_ReportFalse = "^\\*\\* You won't be informed"
  FIBS_ReportTrue = "^\\*\\* You will be informed"
  FIBS_SilentTrue = "^\\*\\* You won't hear what other players shout\\."
  FIBS_SilentFalse = "^\\*\\* You will hear what other players shout\\."
  FIBS_TelnetFalse = "^\\*\\* You use a client program"
  FIBS_TelnetTrue = "^\\*\\* You use telnet"
  FIBS_WrapFalse = "^\\*\\* The server will wrap"
  FIBS_WrapTrue = "^\\*\\* Your terminal knows how to wrap"
  FIBS_PlayerRefusingGames = "^\\*\\* [a-zA-Z_<>]+ is refusing games\\."
  FIBS_NotWatching = "^\\*\\* You're not watching\\."
  FIBS_NotWatchingPlaying = "^\\*\\* You're not watching or playing\\."
  FIBS_NotPlaying = "^\\*\\* You're not playing\\."
  FIBS_NoUser = "^\\*\\* There is no one called "
  FIBS_AlreadyPlaying = "is already playing with"
  FIBS_DidntInvite = "^\\*\\* [a-zA-Z_<>]+ didn't invite you."
  FIBS_BadMove = "^\\*\\* You can't remove this piece"
  FIBS_CantMoveFirstMove = "^\\*\\* You can't move " # ** You can't move 3 points in your first move
  FIBS_CantShout = "^\\*\\* Please type 'toggle silent' again before you shout\\."
  FIBS_MustMove = "^\\*\\* You must give [1-4] moves"
  FIBS_MustComeIn = "^\\*\\* You have to remove pieces from the bar in your first move\\."
  FIBS_UsersHeardYou = "^\\*\\* [0-9]+ users? heard you\\."
  FIBS_Junk = "^\\*\\* Please wait for [a-zA-Z_<>]+ to join too\\."
  FIBS_SavedMatchReady = "^\\*\\*[a-zA-Z_<>]+ +[0-9]+ +[0-9]+ +- +[0-9]+" # double star before a name indicates you have a saved game with this player
  FIBS_NotYourTurnToRoll = "^\\*\\* It's not your turn to roll the dice\\."
  FIBS_NotYourTurnToMove = "^\\*\\* It's not your turn to move\\."
  FIBS_YouStopWatching = "^\\*\\* You stop watching"
  FIBS_UnknownCommand = "^\\*\\* Unknown command:"
  FIBS_CantWatch = "^\\*\\* You can't watch another game while you're playing\\."
  FIBS_CantInviteSelf = "^\\*\\* You can't invite yourself\\."
  FIBS_DontKnowUser = "^\\*\\* Don't know user"
  FIBS_MessageUsage = "^\\*\\* usage: message <user> <text>"
  FIBS_PlayerNotPlaying = "^\\*\\* [a-zA-Z_<>]+ is not playing\\."
  FIBS_CantTalk = "^\\*\\* You can't talk if you won't listen\\."
  FIBS_WontListen = "^\\*\\* [a-zA-Z_<>]+ won't listen to you\\."
  FIBS_Why = "Why would you want to do that" # (not sure about ** vs *** at front of line.)
  FIBS_Ratings = "^\\* *[0-9]+ +[a-zA-Z_<>]+ +[0-9]+\\.[0-9]+ +[0-9]+"
  FIBS_NoSavedMatch = "^\\*\\* There's no saved match with "
  FIBS_WARNINGSavedMatch = "^\\*\\* WARNING: Don't accept if you want to continue"
  FIBS_CantGagYourself = "^\\*\\* You talk too much, don't you\\?"
  FIBS_CantBlindYourself = "^\\*\\* You can't read this message now, can you\\?"


class LoginBatch(CookieDough):
  CLIP_WELCOME = "^1 [a-zA-Z_<>]+ [0-9]+ "
  CLIP_OWN_INFO = "^2 [a-zA-Z_<>]+ [01] [01]"
  CLIP_MOTD_BEGIN = "^3$"
  FIBS_FailedLogin = "^> [0-9]+" # bogus CLIP messages sent after a failed login

class MOTDBatch(CookieDough):
  CLIP_MOTD_END =  "^4$"


if __name__ == '__main__':
  print 'test!'

