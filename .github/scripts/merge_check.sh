#! /bin/bash
BRANCH="template/main"

while [[ $* != '' ]]; do
	  case $1 in
	  "--help" | "-h")
		    echo "
Checks if following code is synchronized with other repo
usage:
	--help, -h      - Display this message
	--repo, -r      - Checked repo
"
		    exit 0
		    ;;
    "--branch" | "-b")
        shift
        BRANCH=$1
        ;;
	  *)
		    echo "Wrong syntax"
		    exit 1
		    ;;
	  esac
	  shift
done

if [[ $BRANCH = "" ]]; then
    echo "Cannot check branch"
    exit 1
fi

EXTERNAL_COMMITS=$(git log --pretty=format:"%H" "${BRANCH}")
CURRENT_COMMITS=$(git log --pretty=format:"%H")

NOT_FOUND=""
for COMMIT in ${EXTERNAL_COMMITS}; do
    echo "Checks commit: ${COMMIT}"
    if ! echo "${CURRENT_COMMITS}" | grep -o "${COMMIT}"; then
        echo "❌ Commit not found in current elements: ${COMMIT}"
        NOT_FOUND="$NOT_FOUND $COMMIT"
    else
        echo "👍 Commit found in current elements: ${COMMIT}"
    fi
done

if [[ "${NOT_FOUND}" != "" ]]; then
    echo ">>>> Not all commits found:"
    for COMMIT in ${NOT_FOUND}; do
        EXTERNAL_MESSAGE=$(git log --pretty=format:"%s" -n 1 "$COMMIT")
        echo "::warning::Commit not synchronize from ${BRANCH} ($COMMIT)"
        echo "❌ Not found : [${EXTERNAL_MESSAGE}]($COMMIT)"
    done
    exit 1
else
    echo ">>>> All commits are merged"
fi
