#pragma once

#include "cmd.h"

class CmdBranchList : public Cmd { public:
	CmdBranchList();
	~CmdBranchList();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
	void v_msgOut(af::Msg& msg) final;
};

class CmdBranchPause : public Cmd { public:
	CmdBranchPause();
	~CmdBranchPause();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBranchStart : public Cmd { public:
	CmdBranchStart();
	~CmdBranchStart();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBranchDelete : public Cmd { public:
	CmdBranchDelete();
	~CmdBranchDelete();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBranchDeleteDone : public Cmd { public:
	CmdBranchDeleteDone();
	~CmdBranchDeleteDone();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBranchLog : public Cmd { public:
	CmdBranchLog();
	~CmdBranchLog();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdJobSetBranch : public Cmd { public:
	CmdJobSetBranch();
	~CmdJobSetBranch();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBlockPause : public Cmd { public:
	CmdBlockPause();
	~CmdBlockPause();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBlockStart : public Cmd { public:
	CmdBlockStart();
	~CmdBlockStart();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBlockDone : public Cmd { public:
	CmdBlockDone();
	~CmdBlockDone();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBlockSkip : public Cmd { public:
	CmdBlockSkip();
	~CmdBlockSkip();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};

class CmdBlockRestart : public Cmd { public:
	CmdBlockRestart();
	~CmdBlockRestart();
	bool v_processArguments(int argc, char** argv, af::Msg &msg) final;
};
