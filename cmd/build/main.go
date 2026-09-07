package main

import (
    "bytes"
    "fmt"
    "io/ioutil"
    "log"
    "os"
    "path/filepath"
    "sort"
    "strings"

    "github.com/tdewolff/minify/v2"
    "github.com/tdewolff/minify/v2/css"
    "github.com/tdewolff/minify/v2/js"
)

// readModules reads all files matching pattern (sorted) and returns concatenated content.
func readModules(dir, pattern string) (string, error) {
    files, err := filepath.Glob(filepath.Join(dir, pattern))
    if err != nil {
        return "", err
    }
    sort.Strings(files)
    var buf bytes.Buffer
    for _, f := range files {
        data, err := os.ReadFile(f)
        if err != nil {
            return "", err
        }
        buf.Write(data)
        buf.WriteString("\n")
    }
    return buf.String(), nil
}

func writeFile(path, content string) error {
    dir := filepath.Dir(path)
    if err := os.MkdirAll(dir, 0o755); err != nil {
        return err
    }
    return os.WriteFile(path, []byte(content), 0o644)
}

func main() {
    // Directories
    cssSrc := filepath.Join("css", "src")
    jsSrc := filepath.Join("js", "src")
    outDir := "dist"

    // Ensure output directories exist
    if err := os.MkdirAll(filepath.Join(outDir, "css"), 0o755); err != nil {
        log.Fatalf("creating css output dir: %v", err)
    }
    if err := os.MkdirAll(filepath.Join(outDir, "js"), 0o755); err != nil {
        log.Fatalf("creating js output dir: %v", err)
    }

    // 1. Process CSS
    cssContent, err := readModules(cssSrc, "*.css")
    if err != nil {
        log.Fatalf("reading CSS modules: %v", err)
    }
    // Write development (unminified) CSS
    devCSSPath := filepath.Join(outDir, "css", "style.css")
    if err := writeFile(devCSSPath, cssContent); err != nil {
        log.Fatalf("writing dev CSS: %v", err)
    }
    // Minify CSS
    m := minify.New()
    m.Add("text/css", &css.Minifier{})
    minCSS, err := m.String("text/css", cssContent)
    if err != nil {
        log.Fatalf("minifying CSS: %v", err)
    }
    prodCSSPath := filepath.Join(outDir, "css", "style.min.css")
    if err := writeFile(prodCSSPath, minCSS); err != nil {
        log.Fatalf("writing min CSS: %v", err)
    }

    // 2. Process JS
    jsContent, err := readModules(jsSrc, "*.js")
    if err != nil {
        log.Fatalf("reading JS modules: %v", err)
    }
    devJSPath := filepath.Join(outDir, "js", "site.js")
    if err := writeFile(devJSPath, jsContent); err != nil {
        log.Fatalf("writing dev JS: %v", err)
    }
    // Minify JS
    m.Add("application/javascript", &js.Minifier{})
    minJS, err := m.String("application/javascript", jsContent)
    if err != nil {
        log.Fatalf("minifying JS: %v", err)
    }
    prodJSPath := filepath.Join(outDir, "js", "site.min.js")
    if err := writeFile(prodJSPath, minJS); err != nil {
        log.Fatalf("writing min JS: %v", err)
    }

    fmt.Printf("✅ Build complete. CSS: %s (%d bytes) → %s (%d bytes)\n", devCSSPath, len(cssContent), prodCSSPath, len(minCSS))
    fmt.Printf("✅ JS: %s (%d bytes) → %s (%d bytes)\n", devJSPath, len(jsContent), prodJSPath, len(minJS))
    // Optional: copy other static assets (images, fonts) – left to existing pipeline.
    _ = outDir // silence unused warning if future code adds more.
    // Print a friendly message for the user.
    fmt.Println("Build artifacts placed in ./dist directory.")
    // End
    if strings.TrimSpace(os.Getenv("CI")) == "true" {
        // In CI environments we may want a non‑zero exit on error – already handled via log.Fatalf.
    }
}
