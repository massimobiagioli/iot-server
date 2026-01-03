from app.repositories.unit_of_work import UnitOfWork


def test_unit_of_work_commit_and_close(mock_session):
    uow = UnitOfWork(mock_session)
    with uow:
        pass
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()
