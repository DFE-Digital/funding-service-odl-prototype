# Design notes

Thoughts and design notes will be kept here.

## Describing changesets

### Describing changes to data

```mermaid
---
title: Models describing how to model changesets to data
---
classDiagram
  class Changeset {
    +Guid Id
    +GitRevision[] Revisions
    +string Description
    +DateTime CreateDateUtc
  }

  class Revision {
    +Guid Id
    +DataChange[] DataChanges
    +string Message
    +DateTime CreateDateUtc
    +string AuthorName
    +string AuthorEmail
  }

  class DataChange {
    +string TableSchema
    +string TableName
    +string ColName
    +string NewColValue
  }

  Changeset --> "1..*" Revision
  Revision --> "1..*" DataChange
```

### Describing changes to DB objects

TODO ...

## Getting a diff between a table present schema/data, and to-be

TODO...

## Tracking multiple revisions to a changeset over time

TODO...