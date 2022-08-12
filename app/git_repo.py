from git import Repo
from git import Git
import os
import shutil

GIT_EXTENSION = ".git"


class Repository(object):
    """
    nap-module GIT repo watcher.
    Clones and watches the repo that contains all the registered NAP modules
    """
    def __init__(self, dir, git_url=None, clean=False):
        """
        initialize GIT repository.
        Clones and watches the repo that contains all the registered NAP modules
        :param dir: where to clone the repo to
        :param git_url: optional link to git repository, cloned when not found
        :param clean: clear module directory before cloning
        """

        self.dir = dir
        self.url = git_url

        # clone if url is specified
        if git_url is not None:
            self._clone(clean)

        # Bind instance of the repo
        self.git = Git(dir)
        self.repo = Repo(dir)
        self.origin = self.repo.remotes.origin

    def _clone(self, clean=False):
        """
        Clones the repo if not on
        :return:
        """

        # Clean if requested
        if os.path.exists(self.dir) and clean:
            shutil.rmtree(self.dir)

        git_dir = "{0}/{1}".format(self.dir, GIT_EXTENSION)
        if not os.path.exists(git_dir):
            print("cloning: {0}".format(self.url))
            Repo.clone_from(self.url, self.dir)

    def pull(self) -> bool:
        """
        Pulls changes if required
        :return If something upstream changed and repo has been updated
        """

        # Fetch remote and get diffs
        self.origin.fetch()
        comp = "{0}/{1}".format(self.origin.name, self.repo.active_branch)

        # Bail if changes are local
        commits = "{0}..{1}".format(self.repo.active_branch, comp)
        commits_behind = list(self.repo.iter_commits(commits))
        if len(commits_behind) == 0:
            print("{0}: no remote changes".format(comp))
            return False

        # Notify and pull
        print("{0}: has changes".format(comp))
        for commit in commits_behind:
            print("applying commit: {0}".format(commit.summary))
        self.origin.pull()
        return True

    def push(self, message):
        """
        Push all local changes to remote
        :return If something upstream changed and repo has been updated
        """
        self.repo.git.add(all=True)
        self.repo.index.commit(message)
        self.repo.remote(self.origin.name).push()

    def checkout(self, tag):
        self.git.checkout(tag)


