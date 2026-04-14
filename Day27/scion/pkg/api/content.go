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
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// ResolveContent resolves a content field value using the file:// URI convention.
//
// Resolution rules:
//   - "file:///absolute/path" — read from absolute file path
//   - "file://relative/path" — read from path relative to configDir
//   - Any other value — treated as inline content (returned as-is)
//
// Returns empty string and nil error for empty input.
func ResolveContent(value string, configDir string) (string, error) {
	if value == "" {
		return "", nil
	}

	if strings.HasPrefix(value, "file:///") {
		filePath := strings.TrimPrefix(value, "file:///")
		// Restore leading slash for absolute path
		filePath = "/" + filePath
		content, err := os.ReadFile(filePath)
		if err != nil {
			return "", fmt.Errorf("failed to read content file %s: %w", filePath, err)
		}
		return string(content), nil
	}

	if strings.HasPrefix(value, "file://") {
		relPath := strings.TrimPrefix(value, "file://")
		absPath := filepath.Join(configDir, relPath)
		content, err := os.ReadFile(absPath)
		if err != nil {
			return "", fmt.Errorf("failed to read content file %s: %w", absPath, err)
		}
		return string(content), nil
	}

	// No file:// prefix — treat as inline content
	return value, nil
}
