package fswatcher

import "testing"

func TestIsWorkspaceMount(t *testing.T) {
	tests := []struct {
		dest string
		want bool
	}{
		{"/workspace", true},
		{"/repo-root", true},
		{"/repo-root/.scion/agents/my-agent/workspace", true},
		{"/repo-root/.scion/agents/foo/workspace", true},
		{"/home/user/workspace", false},
		{"/home/gemini", false},
		{"/tmp", false},
		{"/repo-root/.scion/agents/foo/home", false},
		{"", false},
	}
	for _, tt := range tests {
		t.Run(tt.dest, func(t *testing.T) {
			got := isWorkspaceMount(tt.dest)
			if got != tt.want {
				t.Errorf("isWorkspaceMount(%q) = %v, want %v", tt.dest, got, tt.want)
			}
		})
	}
}
