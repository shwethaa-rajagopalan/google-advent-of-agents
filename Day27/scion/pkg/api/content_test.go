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

package api

import (
	"os"
	"path/filepath"
	"testing"
)

func TestResolveContent_Empty(t *testing.T) {
	result, err := ResolveContent("", "/tmp")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != "" {
		t.Fatalf("expected empty string, got %q", result)
	}
}

func TestResolveContent_InlineContent(t *testing.T) {
	content := "You are a code reviewer."
	result, err := ResolveContent(content, "/tmp")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != content {
		t.Fatalf("expected %q, got %q", content, result)
	}
}

func TestResolveContent_AbsoluteFileURI(t *testing.T) {
	dir := t.TempDir()
	filePath := filepath.Join(dir, "prompt.md")
	expected := "absolute file content"
	if err := os.WriteFile(filePath, []byte(expected), 0644); err != nil {
		t.Fatalf("failed to write test file: %v", err)
	}

	uri := "file://" + filePath
	result, err := ResolveContent(uri, "/some/other/dir")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != expected {
		t.Fatalf("expected %q, got %q", expected, result)
	}
}

func TestResolveContent_RelativeFileURI(t *testing.T) {
	dir := t.TempDir()
	subDir := filepath.Join(dir, "prompts")
	if err := os.MkdirAll(subDir, 0755); err != nil {
		t.Fatalf("failed to create subdir: %v", err)
	}
	filePath := filepath.Join(subDir, "system.md")
	expected := "relative file content"
	if err := os.WriteFile(filePath, []byte(expected), 0644); err != nil {
		t.Fatalf("failed to write test file: %v", err)
	}

	result, err := ResolveContent("file://prompts/system.md", dir)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != expected {
		t.Fatalf("expected %q, got %q", expected, result)
	}
}

func TestResolveContent_FileNotFound(t *testing.T) {
	_, err := ResolveContent("file:///nonexistent/path/file.md", "/tmp")
	if err == nil {
		t.Fatal("expected error for nonexistent file, got nil")
	}
}

func TestResolveContent_RelativeFileNotFound(t *testing.T) {
	_, err := ResolveContent("file://nonexistent.md", t.TempDir())
	if err == nil {
		t.Fatal("expected error for nonexistent relative file, got nil")
	}
}

func TestResolveContent_MultilineInline(t *testing.T) {
	content := "Line 1\nLine 2\nLine 3"
	result, err := ResolveContent(content, "/tmp")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != content {
		t.Fatalf("expected multiline content, got %q", result)
	}
}
