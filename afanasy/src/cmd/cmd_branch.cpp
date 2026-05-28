#include "cmd_branch.h"

#include <iostream>

#include "../libafanasy/msgclasses/mcafnodes.h"

#define AFOUTPUT
#undef AFOUTPUT
#include "../include/macrooutput.h"

// ─── blist ───────────────────────────────────────────────────────────────────

CmdBranchList::CmdBranchList()
{
	setCmd("blist");
	setInfo("List of branches.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchList::~CmdBranchList() {}
bool CmdBranchList::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	m_str << "{\"get\":{\"type\":\"branches\"}}";
	return true;
}
void CmdBranchList::v_msgOut(af::Msg& msg)
{
	af::MCAfNodes list(&msg);
	list.v_stdOut();
}

// ─── bpause ──────────────────────────────────────────────────────────────────

CmdBranchPause::CmdBranchPause()
{
	setCmd("bpause");
	setArgsCount(1);
	setInfo("Pause a branch.");
	setHelp("bpause [path] Pause the branch at the given path.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchPause::~CmdBranchPause() {}
bool CmdBranchPause::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	std::string path = argv[0];
	af::jsonActionOperation(m_str, "branches", "pause", path);
	return true;
}

// ─── bstart ──────────────────────────────────────────────────────────────────

CmdBranchStart::CmdBranchStart()
{
	setCmd("bstart");
	setArgsCount(1);
	setInfo("Unpause (start) a branch.");
	setHelp("bstart [path] Unpause the branch at the given path.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchStart::~CmdBranchStart() {}
bool CmdBranchStart::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	std::string path = argv[0];
	af::jsonActionOperation(m_str, "branches", "start", path);
	return true;
}

// ─── bdelete ─────────────────────────────────────────────────────────────────

CmdBranchDelete::CmdBranchDelete()
{
	setCmd("bdelete");
	setArgsCount(1);
	setInfo("Delete an empty branch.");
	setHelp("bdelete [path] Delete the branch at the given path. Branch must have no child branches or jobs.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchDelete::~CmdBranchDelete() {}
bool CmdBranchDelete::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	std::string path = argv[0];
	af::jsonActionOperation(m_str, "branches", "delete", path);
	return true;
}

// ─── bdeldone ────────────────────────────────────────────────────────────────

CmdBranchDeleteDone::CmdBranchDeleteDone()
{
	setCmd("bdeldone");
	setArgsCount(1);
	setInfo("Delete done jobs from a branch.");
	setHelp("bdeldone [path] Remove all done jobs from the branch at the given path.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchDeleteDone::~CmdBranchDeleteDone() {}
bool CmdBranchDeleteDone::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	std::string path = argv[0];
	af::jsonActionOperation(m_str, "branches", "delete_done_jobs", path);
	return true;
}

// ─── blog ────────────────────────────────────────────────────────────────────

CmdBranchLog::CmdBranchLog()
{
	setCmd("blog");
	setArgsCount(1);
	setInfo("Get branch log.");
	setHelp("blog [id] Get branch log for the branch with the given numeric id.");
	setMsgType(af::Msg::TJSON);
}
CmdBranchLog::~CmdBranchLog() {}
bool CmdBranchLog::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	int branch_id = atoi(argv[0]);
	m_str << "{\"get\":{\"type\":\"branches\",\"mode\":\"log\",\"ids\":[" << branch_id << "]}}";
	return true;
}

// ─── jbranch ─────────────────────────────────────────────────────────────────

CmdJobSetBranch::CmdJobSetBranch()
{
	setCmd("jbranch");
	setArgsCount(2);
	setInfo("Move job(s) to a different branch.");
	setHelp("jbranch [job_mask] [branch_path] Move all jobs matching the mask into the given branch path.");
	setMsgType(af::Msg::TJSON);
}
CmdJobSetBranch::~CmdJobSetBranch() {}
bool CmdJobSetBranch::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	std::string job_mask    = argv[0];
	std::string branch_path = argv[1];

	af::jsonActionParamsStart(m_str, "jobs", job_mask);
	m_str << "\n\"branch\":\"" << branch_path << '"';
	af::jsonActionParamsFinish(m_str);

	return true;
}

// ─── block helpers ────────────────────────────────────────────────────────────

static void buildBlockOperation(std::ostringstream & o_str,
                                 const std::string & job_mask,
                                 const std::string & block_mask,
                                 const std::string & operation_type)
{
	af::jsonActionStart(o_str, "jobs", job_mask, std::vector<int>());
	o_str << ",\n\"block_mask\":\"" << block_mask << '"';
	o_str << ",\n\"operation\":{\"type\":\"" << operation_type << "\"}";
	af::jsonActionFinish(o_str);
}

// ─── blkpause ────────────────────────────────────────────────────────────────

CmdBlockPause::CmdBlockPause()
{
	setCmd("blkpause");
	setArgsCount(2);
	setInfo("Suspend (pause) blocks matching a mask inside jobs matching a mask.");
	setHelp("blkpause [job_mask] [block_mask] Suspend matching blocks.");
	setMsgType(af::Msg::TJSON);
}
CmdBlockPause::~CmdBlockPause() {}
bool CmdBlockPause::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	buildBlockOperation(m_str, argv[0], argv[1], "suspend");
	return true;
}

// ─── blkstart ────────────────────────────────────────────────────────────────

CmdBlockStart::CmdBlockStart()
{
	setCmd("blkstart");
	setArgsCount(2);
	setInfo("Continue (unpause) blocks matching a mask inside jobs matching a mask.");
	setHelp("blkstart [job_mask] [block_mask] Continue (resume) matching blocks.");
	setMsgType(af::Msg::TJSON);
}
CmdBlockStart::~CmdBlockStart() {}
bool CmdBlockStart::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	buildBlockOperation(m_str, argv[0], argv[1], "continue");
	return true;
}

// ─── blkdone ─────────────────────────────────────────────────────────────────

CmdBlockDone::CmdBlockDone()
{
	setCmd("blkdone");
	setArgsCount(2);
	setInfo("Mark all tasks in matching blocks as done.");
	setHelp("blkdone [job_mask] [block_mask] Mark all tasks in matching blocks as done.");
	setMsgType(af::Msg::TJSON);
}
CmdBlockDone::~CmdBlockDone() {}
bool CmdBlockDone::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	buildBlockOperation(m_str, argv[0], argv[1], "done");
	return true;
}

// ─── blkskip ─────────────────────────────────────────────────────────────────

CmdBlockSkip::CmdBlockSkip()
{
	setCmd("blkskip");
	setArgsCount(2);
	setInfo("Skip all tasks in matching blocks.");
	setHelp("blkskip [job_mask] [block_mask] Skip all tasks in matching blocks.");
	setMsgType(af::Msg::TJSON);
}
CmdBlockSkip::~CmdBlockSkip() {}
bool CmdBlockSkip::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	buildBlockOperation(m_str, argv[0], argv[1], "skip");
	return true;
}

// ─── blkrestart ──────────────────────────────────────────────────────────────

CmdBlockRestart::CmdBlockRestart()
{
	setCmd("blkrestart");
	setArgsCount(2);
	setInfo("Restart all tasks in matching blocks.");
	setHelp("blkrestart [job_mask] [block_mask] Restart all tasks in matching blocks.");
	setMsgType(af::Msg::TJSON);
}
CmdBlockRestart::~CmdBlockRestart() {}
bool CmdBlockRestart::v_processArguments(int argc, char** argv, af::Msg &msg)
{
	buildBlockOperation(m_str, argv[0], argv[1], "restart");
	return true;
}
