# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

import rq
from crum import get_current_request, get_current_user

if TYPE_CHECKING:
    from cvat.apps.engine.models import User


def get_user(instance=None) -> User | dict | None:
    def _get_user_from_rq_job(rq_job: rq.job.Job) -> dict | None:
        from cvat.apps.engine.rq import BaseRQMeta

        if user := BaseRQMeta.for_job(rq_job).user:
            return user.to_dict()
        return None

    user = get_current_user()
    if user is not None:
        return user

    if isinstance(instance, rq.job.Job):
        return _get_user_from_rq_job(instance)

    if rq_job := rq.get_current_job():
        return _get_user_from_rq_job(rq_job)

    from cvat.apps.engine.models import User

    if isinstance(instance, User):
        return instance

    return None


def get_request(instance=None):
    def _get_request_from_rq_job(rq_job: rq.job.Job) -> dict | None:
        from cvat.apps.engine.rq import BaseRQMeta

        if request := BaseRQMeta.for_job(rq_job).request:
            return request.to_dict()
        return None

    request = get_current_request()
    if request is not None:
        return request

    if isinstance(instance, rq.job.Job):
        return _get_request_from_rq_job(instance)

    if rq_job := rq.get_current_job():
        return _get_request_from_rq_job(rq_job)

    return None
