# Cross-Team Requirement Form Design

Date: 2026-03-27

## Goal

Create a requirement collection package that helps other project groups clearly state:

- what they want the system to do
- what data, devices, documents, or interfaces they can provide
- what kind of collaboration they expect from our team

The package will be used in two stages:

1. each group fills in its own form first
2. the team reviews the returned forms together in a follow-up meeting

The main purpose is cross-team alignment first, then development prioritization.

## Target Groups

The forms will be created for these four groups:

- Water treatment group
- Drainage group
- Application group
- Derection group

## Final Deliverables

The final output will be 8 Word documents:

### Chinese version

- `水处理组需求采集表.docx`
- `排水组需求采集表.docx`
- `应用组需求采集表.docx`
- `Derection组需求采集表.docx`

### English version

- `Water_Treatment_Group_Requirement_Form.docx`
- `Drainage_Group_Requirement_Form.docx`
- `Application_Group_Requirement_Form.docx`
- `Derection_Group_Requirement_Form.docx`

## Chosen Approach

Use one shared form structure with group-specific prompts.

This means:

- all groups receive forms with the same high-level structure
- each group gets tailored guidance based on its role
- the returned forms remain easy to compare across groups

This is preferred over four unrelated forms because it preserves consistency for later review and planning.

## Form Structure

Each document will contain the following sections.

### 1. Title

The title clearly states which group the form is for.

Examples:

- `Water treatment group requirement collection form`
- `水处理组需求采集表`

### 2. Purpose

A short bilingual introduction explains that the form is used to collect both:

- business needs
- technical coordination details

The introduction should make clear that the goal is to help define future collaboration and system work.

### 3. Instructions

Each form will explain:

- one group should fill in one form
- Part A is filled in once per group
- Part B can contain multiple requirement items
- rough or partial answers are acceptable if details are not final yet
- the form will be reviewed again in a meeting later

### 4. Part A. Group Overview

This section captures the overall collaboration context for the group.

Recommended fields:

- Group name
- Main responsibility
- Current progress or existing outputs
- What support is needed from our system
- What the group can provide
- Related devices, data, documents, or interfaces
- Main contact person
- Preferred collaboration method

### 5. Part B. Requirement Items

This section captures multiple specific requests from the group.

Recommended fields:

- Requirement title
- Problem to solve
- Expected function
- Input needed
- Who provides the input
- Expected output
- Target users
- Priority
- Preferred timeline
- Dependencies or risks
- Remarks

This section should be designed as a repeatable table so one group can list multiple needs.

### 6. Group-Specific Hints

Each form will include short guidance that matches the target group.

The purpose is to help the group write concrete, useful requirements instead of vague requests.

### 7. Follow-Up Note

The document ends with a short note explaining that unclear items can be discussed and confirmed in the later review meeting.

## Group-Specific Guidance

### Water treatment group

This form should guide the group toward:

- water quality indicators
- treatment stages to reflect in the system
- alert thresholds
- historical trend records
- treatment-result comparison
- available monitoring data

### Drainage group

This form should guide the group toward:

- drainage points that need monitoring
- abnormal drainage conditions
- real-time versus periodic records
- route or area visibility
- field data and device data they can provide

### Application group

This form should guide the group toward:

- target users
- key operations users must complete
- important pages or modules
- information hierarchy
- current usability issues

### Derection group

This form should guide the group toward:

- decision-making information needs
- summary dashboards or reports
- highlighted indicators
- update frequency expectations
- outputs useful for meetings or presentations

## Document Style

The final Word documents should be:

- clean and formal
- easy to fill in
- structured with tables rather than long free-text blocks
- suitable for sending directly to other groups

The Chinese and English versions should be equivalent in structure, not just loosely translated.

## Usage Flow

The intended process is:

1. send each group its corresponding form
2. ask each group to complete it independently
3. collect all returned forms
4. review them internally first
5. hold a follow-up meeting to clarify unclear items
6. convert confirmed results into a development and coordination list

## Scope Boundaries

This work covers:

- designing the structure of the forms
- preparing bilingual Word templates
- tailoring prompts for each of the four groups

This work does not yet cover:

- turning the forms into an online survey
- converting the returned forms into a final roadmap
- implementing any project features mentioned by those groups

## Recommendation

Proceed with 8 Word templates based on one shared bilingual structure and four group-specific prompt sets.

This gives the team a consistent way to gather both feature requests and technical coordination details while keeping each form relevant to the target group.
