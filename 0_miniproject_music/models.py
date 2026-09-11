"""
    Song, Podcast 등 도메인 클래스
"""
class Music():
    """부모 클래스: 음악"""
    id = 1
    # Constructor
    def __init__(self, title, artist = "Unknown", track_length = 90):
        self.id = Music.id
        Music.id += 1
        self.title = title
        self.artist = artist
        self.track_length = track_length
        self.tl = f"{self.track_length // 60}:{self.track_length % 60}"

    # __str__
    def __str__(self):
        """print() 또는 str() 호출 시 가독성 좋은 문자열 반환"""
        return f"ID: {self.id} | [{self.title}] {self.artist} {self.tl}"

    # 재생
    def play(self):
        """재생 시 반환할 문자열"""
        return f"ID: {self.id} | [{self.title}] {self.artist} {self.tl}를 재생 중입니다."

class Song(Music):
    """자식 클래스: 노래"""
    def __init__(self, title, artist = "Unknown", track_length = 90, lyrics = "No Lyrics"):
        super().__init__(title, artist, track_length)
        self.lyrics = lyrics

    # 재생
    def play(self):
        return f"""
        ID: {self.id} | [{self.title}] {self.artist} {self.tl}
        (가사: {self.lyrics[:20]}...)를 재생 중입니다."""

class Podcast(Music):
    """자식 클래스: 팟캐스트"""
    def __init__(self, title, artist = "Unknown", track_length = 90, host = "host", ep_num = 0):
        super().__init__(title, artist, track_length)
        self.ep_num = ep_num
        self.host = host

    # 재생
    def play(self):
        return f"""
        ID: {self.id} | [{self.title}] {self.artist} {self.tl}
        {self.host}의 {self.ep_num}번 에피소드의 곡을 재생 중입니다.)"""

class MusicNotFoundError(Exception):
    """음악을 찾을 수 없을 떄 발생하는 예외"""
    def __init__(self, id):
        super().__init__("음악을 찾을 수 없습니다.")
        self.id = id

class DuplicateMusicError(Exception):
    def __init__(self, id):
        super().__init__("이미 추가한 곡입니다.")
        self.id = id

class NoMusicInListError(Exception):
    def __init__(self, list):
        super().__init__("플레이리스트에 추가된 곡이 없습니다.")
        self.list = list