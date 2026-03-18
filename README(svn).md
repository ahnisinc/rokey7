SVN 방식 (파일/폴더 바로 다운로드)
✔️ 설치 방법
sudo apt update
sudo apt install subversion

svn --version

svn checkout <url>
svn export <url>
svn update

GitHub도 SVN 프로토콜 지원 → 특정 폴더만 다운로드 가능

svn export https://github.com/user/repo/trunk/폴더경로
trunk/폴더경로 부분에 원하는 서브폴더 경로 지정

✔️ 예시
특정 파일 다운로드
svn export https://github.com/username/repo/trunk/path/to/file.py

다운로드한 파일은 현재 폴더에 저장

wget https://github.com/username/repo/archive/refs/heads/main.zip