<INSTRUCTION immutable>

## Documentation Standards

These standards ensure consistent and effective documentation across the project, particularly for agent-assisted development.

### General Principles

1. **Clarity First**
   - Write clear, concise documentation
   - Use simple language and avoid jargon
   - Include examples for complex concepts
   - Keep paragraphs focused and brief

2. **Structure and Organization**
   - Use consistent markdown formatting
   - Follow a logical hierarchy of headings
   - Include a table of contents for longer documents
   - Group related information together

3. **Version Control**
   - All documentation is version controlled
   - Include creation/update dates where relevant
   - Use meaningful commit messages
   - Track major changes in change logs

### File Naming

1. **Memory Files**
   - Use ISO date prefixes: `YYYY-MM-DD-title.md`
   - Use lowercase with hyphens for titles
   - Be descriptive but concise
   - Examples:
     - `2024-03-28-auth-implementation.md`
     - `2024-03-29-performance-optimization.md`

2. **Context Files**
   - Use clear, purpose-indicating names
   - Stick to lowercase with hyphens
   - Keep names short but meaningful
   - Examples:
     - `architecture.md`
     - `coding-standards.md`
     - `deployment-guide.md`

### Content Types

1. **Immutable Content**
   ```markdown
   <INSTRUCTION immutable>
   Content that should never be modified
   </INSTRUCTION>
   ```

2. **Append-Only Logs**
   ```markdown
   <LOG append>
   Chronological updates and changes
   </LOG>
   ```

3. **Task Lists**
   ```markdown
   - [ ] Pending task
   - [x] Completed task
   ```

### Documentation Categories

1. **Context Documentation**
   - Project goals and constraints
   - Architectural decisions
   - Technical standards
   - Development guidelines

2. **Memory Documentation**
   - Technical decisions and rationales
   - Progress updates and milestones
   - Learnings and insights
   - Implementation details

3. **Workspace Documentation**
   - Current task details
   - Implementation plans
   - Validation criteria
   - Working notes

### Best Practices

1. **Maintenance**
   - Review and update regularly
   - Remove outdated information
   - Keep formatting consistent
   - Fix broken links promptly

2. **Content Quality**
   - Be specific and accurate
   - Include relevant context
   - Use proper grammar and spelling
   - Validate technical accuracy

3. **Accessibility**
   - Use proper heading hierarchy
   - Include alt text for images
   - Use descriptive link text
   - Maintain good contrast

4. **Knowledge Sharing**
   - Document assumptions
   - Explain complex decisions
   - Include troubleshooting guides
   - Share learned lessons

</INSTRUCTION>

<LOG append>
# Documentation Standards Updates

Record any clarifications or additions to documentation standards here:

</LOG>