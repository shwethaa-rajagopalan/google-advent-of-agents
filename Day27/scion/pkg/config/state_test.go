// Copyright 2026 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package config

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestLoadGroveState_NonExistent(t *testing.T) {
	tmpDir := t.TempDir()
	state, err := LoadGroveState(tmpDir)
	require.NoError(t, err)
	assert.Equal(t, "", state.LastSyncedAt)
}

func TestSaveAndLoadGroveState_RoundTrip(t *testing.T) {
	tmpDir := t.TempDir()
	grovePath := filepath.Join(tmpDir, ".scion")
	require.NoError(t, os.MkdirAll(grovePath, 0755))

	// Save state
	state := &GroveState{LastSyncedAt: "2026-02-16T10:30:00Z"}
	err := SaveGroveState(grovePath, state)
	require.NoError(t, err)

	// Verify file exists
	_, err = os.Stat(filepath.Join(grovePath, "state.yaml"))
	require.NoError(t, err)

	// Load state back
	loaded, err := LoadGroveState(grovePath)
	require.NoError(t, err)
	assert.Equal(t, "2026-02-16T10:30:00Z", loaded.LastSyncedAt)
}

func TestSaveGroveState_OverwritesExisting(t *testing.T) {
	tmpDir := t.TempDir()
	grovePath := filepath.Join(tmpDir, ".scion")
	require.NoError(t, os.MkdirAll(grovePath, 0755))

	// Save initial state
	state1 := &GroveState{LastSyncedAt: "2026-02-16T10:30:00Z"}
	require.NoError(t, SaveGroveState(grovePath, state1))

	// Save updated state
	state2 := &GroveState{LastSyncedAt: "2026-02-16T11:00:00Z"}
	require.NoError(t, SaveGroveState(grovePath, state2))

	// Verify updated value
	loaded, err := LoadGroveState(grovePath)
	require.NoError(t, err)
	assert.Equal(t, "2026-02-16T11:00:00Z", loaded.LastSyncedAt)
}

func TestSaveGroveState_CreatesDirectoryIfNeeded(t *testing.T) {
	tmpDir := t.TempDir()
	grovePath := filepath.Join(tmpDir, "nested", "path", ".scion")

	state := &GroveState{LastSyncedAt: "2026-02-16T10:30:00Z"}
	err := SaveGroveState(grovePath, state)
	require.NoError(t, err)

	loaded, err := LoadGroveState(grovePath)
	require.NoError(t, err)
	assert.Equal(t, "2026-02-16T10:30:00Z", loaded.LastSyncedAt)
}

func TestLoadGroveState_EmptyFile(t *testing.T) {
	tmpDir := t.TempDir()
	grovePath := filepath.Join(tmpDir, ".scion")
	require.NoError(t, os.MkdirAll(grovePath, 0755))

	// Write empty file
	require.NoError(t, os.WriteFile(filepath.Join(grovePath, "state.yaml"), []byte(""), 0644))

	state, err := LoadGroveState(grovePath)
	require.NoError(t, err)
	assert.Equal(t, "", state.LastSyncedAt)
}
