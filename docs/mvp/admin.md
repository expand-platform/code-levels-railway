Suggestions for a Better Editor:

Django Admin Customization:

Use TabularInline for chapters within projects and for ChapterPart within chapters.
Register ChapterPart in the admin to allow direct editing of order and custom titles.
Consider using django-nested-admin for true nested inlines (chapters with parts inline).
Rich Content Editing:

For editing part content, use a WYSIWYG editor like django-ckeditor or django-summernote.
These can be integrated into your admin for rich text, images, and media.
Bulk/Drag-and-Drop Ordering:

For easier ordering, use django-admin-sortable2 or similar packages to enable drag-and-drop ordering of chapters and parts.