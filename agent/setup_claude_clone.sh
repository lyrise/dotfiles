for name in freetoken ollama openrouter; do
  dir="$HOME/.claude-$name"

  mkdir -p "$dir"
  ln -sfn "$HOME/.claude/skills" "$dir/skills"
done
