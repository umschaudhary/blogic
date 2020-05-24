(PENDING, APPROVED, DENIED, DRAFT,
 PUBLISHED, SCHEDULED, EXPIRED, DELETED) = ('Pending', 'Approved',
                                            'Denied', 'Draft', 'Published',
                                            'Scheduled', 'Expired', 'Deleted'
                                            )
(ONLY_ME, PUBLIC, FOLLOWERS) = ("Only me", "Public", "Followers")

STATUS_CHOICES = (
    (DRAFT, DRAFT),
    (PENDING, PENDING),
    (DENIED, DENIED),
    (PUBLISHED, PUBLISHED),
    (SCHEDULED, SCHEDULED),
    (EXPIRED, EXPIRED),
    (DELETED, DELETED),
)

PRIVACY_CHOICES = (
    (ONLY_ME, ONLY_ME),
    (PUBLIC, PUBLIC),
    (FOLLOWERS, FOLLOWERS),
)
