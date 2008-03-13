/*
 * ---  FIBSCookieMonster.h --------------------------------------------------
 *
 *  Created by Paul Ferguson on Tue Dec 24 2002.
 *  Copyright (c) 2003 Paul Ferguson. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * * Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright
 *   notice, this list of conditions and the following disclaimer in the
 *   documentation and/or other materials provided with the distribution.
 *
 * * The name of Paul D. Ferguson may not be used to endorse or promote
 *   products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
 * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ---------------------------------------------------------------------------
 *
 * Refer to FIBSCookieMonster.html for programming notes about this file.
 *
 * ---------------------------------------------------------------------------
 */

#pragma once

#include "clip.h"

// The public functions exported by FIBSCookieMonster

int  FIBSCookie(const char * nextMessage);
void ResetFIBSCookieMonster();
void ReleaseFIBSCookieMonster();


typedef enum
{
	FIBS_BAD_COOKIE = -1,			// indicates the cookie monster failed to initialize properly

	// implicitly includes CLIP message IDs, in range 1..19, see clip.h
	
	FIBS_PreLogin = CLIP_LAST_CLIP_ID + 1,	// the ASCII "FIBS" art, etc.
	FIBS_LoginPrompt,
	FIBS_FailedLogin,				// use this to detect a failed login (e.g. wrong password)
	FIBS_MOTD,
	FIBS_Goodbye,
	FIBS_PostGoodbye,				// "send cookies", etc.
	FIBS_Unknown,					// don't know the type, probably can ignore
	FIBS_Empty,						// empty string
	FIBS_Junk,						// a message we don't care about, but is not unknown
	FIBS_ClearScreen,
	FIBS_BAD_AcceptDouble,			// DANGER, WILL ROBINSON!!! See notes in .c file about these two cookies!
	FIBS_BAD_Board,	
	FIBS_Average,
	FIBS_DiceTest,
	FIBS_Stat,
	FIBS_Why,
	FIBS_NoInfo,
	FIBS_LastLogout,
	FIBS_RatingCalcStart,
	FIBS_RatingCalcInfo,
	FIBS_SettingsHeader,
	FIBS_PlayerListHeader,
	FIBS_AwayListHeader,
	FIBS_RatingExperience,
	FIBS_NotLoggedIn,
	FIBS_StillLoggedIn,
	FIBS_NoOneIsAway,
	FIBS_RatingsHeader,
	FIBS_IsPlayingWith,
	FIBS_Timeout,
	FIBS_UnknownCommand,
	FIBS_Username,
	FIBS_LastLogin,
	FIBS_YourLastLogin,
	FIBS_Registered,
	FIBS_ONEUSERNAME,
	FIBS_EnterUsername,
	FIBS_EnterPassword,
	FIBS_TypeInNo,
	FIBS_SavedScoreHeader,
	FIBS_NoSavedGames,
	FIBS_UsersHeardYou,
	FIBS_MessagesForYou,
	FIBS_IsAway,
	FIBS_OpponentLogsOut,
	FIBS_Waves,
	FIBS_WavesAgain,
	FIBS_YouGag,
	FIBS_YouUngag,
	FIBS_YouBlind,
	FIBS_YouUnblind,
	FIBS_WatchResign,
	FIBS_UseToggleReady,
	FIBS_WARNINGSavedMatch,
	FIBS_NoSavedMatch,
	FIBS_AlreadyPlaying,
	FIBS_DidntInvite,
	FIBS_WatchingHeader,
	FIBS_NotWatching,
	FIBS_NotWatchingPlaying,
	FIBS_NotPlaying,
	FIBS_PlayerNotPlaying,
	FIBS_NoUser,
	FIBS_CantInviteSelf,
	FIBS_CantWatch,
	FIBS_CantTalk,
	FIBS_CantBlindYourself,
	FIBS_CantGagYourself,
	FIBS_WontListen,
	FIBS_TypeBack,
	FIBS_NoOne,
	FIBS_BadMove,
	FIBS_MustMove,
	FIBS_MustComeIn,
	FIBS_CantShout,
	FIBS_DontKnowUser,
	FIBS_MessageUsage,
	FIBS_Done,
	FIBS_SavedMatchesHeader,
	FIBS_NotYourTurnToRoll,
	FIBS_NotYourTurnToMove,
	FIBS_YourTurnToMove,
	FIBS_Ratings,
	FIBS_PlayerInfoStart,
	FIBS_EmailAddress,
	FIBS_NoEmail,
	FIBS_ListOfGames,
	FIBS_SavedMatch,
	FIBS_SavedMatchPlaying,
	FIBS_SavedMatchReady,
	FIBS_YouAreWatching,
	FIBS_YouStopWatching,
	FIBS_PlayerStartsWatching,
	FIBS_PlayerStopsWatching,
	FIBS_PlayerIsWatching,
	FIBS_ReportUnlimitedMatch,
	FIBS_ReportLimitedMatch,
	FIBS_RollOrDouble,
	FIBS_YouWinMatch,
	FIBS_PlayerWinsMatch,
	FIBS_YouReject,
	FIBS_YouResign,
	FIBS_ResumeMatchRequest,
	FIBS_ResumeMatchAck0,
	FIBS_ResumeMatchAck5,
	FIBS_NewMatchRequest,
	FIBS_UnlimitedInvite,
	FIBS_YouInvited,
	FIBS_NewMatchAck9,
	FIBS_NewMatchAck10,
	FIBS_NewMatchAck2,
	FIBS_YouTerminated,
	FIBS_OpponentLeftGame,
	FIBS_PlayerLeftGame,
	FIBS_PlayerRefusingGames,
	FIBS_TypeJoin,
	FIBS_ShowMovesStart,
	FIBS_ShowMovesWins,
	FIBS_ShowMovesRoll,
	FIBS_ShowMovesDoubles,
	FIBS_ShowMovesAccepts,
	FIBS_ShowMovesRejects,
	FIBS_ShowMovesOther,
	FIBS_Board,
	FIBS_YouRoll,
	FIBS_PlayerRolls,
	FIBS_PlayerMoves,
	FIBS_Doubles,
	FIBS_AcceptRejectDouble,
	FIBS_StartingNewGame,
	FIBS_PlayerAcceptsDouble,
	FIBS_YouAcceptDouble,
	FIBS_Settings,
	FIBS_Turn,
	FIBS_FirstRoll,
	FIBS_DoublingCubeNow,
	FIBS_CantMove,
	FIBS_CantMoveFirstMove,
	FIBS_ResignRefused,
	FIBS_YouWinGame,
	FIBS_OnlyPossibleMove,
	FIBS_AcceptWins,
	FIBS_ResignWins,
	FIBS_ResignYouWin,
	FIBS_WatchGameWins,
	FIBS_ScoreUpdate,
	FIBS_MatchStart,
	FIBS_YouAcceptAndWin,
	FIBS_OnlyMove,
	FIBS_BearingOff,
	FIBS_PleaseMove,
	FIBS_MakesFirstMove,
	FIBS_YouDouble,
	FIBS_MatchLength,
	FIBS_PlayerWantsToResign,
	FIBS_PlayerWinsGame,
	FIBS_JoinNextGame,
	FIBS_ResumingUnlimitedMatch,
	FIBS_ResumingLimitedMatch,
	FIBS_PlayersStartingMatch,
	FIBS_PlayersStartingUnlimitedMatch,
	FIBS_MatchResult,
	FIBS_YouGiveUp,
	FIBS_PlayerIsWaitingForYou,
	FIBS_Boardstyle,
	FIBS_Linelength,
	FIBS_Pagelength,
	FIBS_Redoubles,
	FIBS_Sortwho,
	FIBS_Timezone,
	FIBS_RedoublesSetTo,
	FIBS_AllowpipTrue,
	FIBS_AllowpipFalse,
	FIBS_AutoboardTrue,
	FIBS_AutoboardFalse,
	FIBS_AutodoubleTrue,
	FIBS_AutodoubleFalse,
	FIBS_AutomoveTrue,
	FIBS_AutomoveFalse,
	FIBS_BellTrue,
	FIBS_BellFalse,
	FIBS_CrawfordTrue,
	FIBS_CrawfordFalse,
	FIBS_DoubleTrue,
	FIBS_DoubleFalse,
	FIBS_MoreboardsTrue,
	FIBS_MoreboardsFalse,
	FIBS_MovesTrue,
	FIBS_MovesFalse,
	FIBS_GreedyTrue,
	FIBS_GreedyFalse,
	FIBS_NotifyTrue,
	FIBS_NotifyFalse,
	FIBS_RatingsTrue,
	FIBS_RatingsFalse,
	FIBS_ReadyTrue,
	FIBS_ReadyFalse,
	FIBS_ReportTrue,
	FIBS_ReportFalse,
	FIBS_SilentTrue,
	FIBS_SilentFalse,
	FIBS_TelnetTrue,
	FIBS_TelnetFalse,
	FIBS_WrapTrue,
	FIBS_WrapFalse,
	FIBS_LastMessage	// NO MORE MESSAGES HERE!
} FIBS_Cookies;
