"""
    곡 목록 관리 클래스 (CRUD)
    DAO / Mapper 역할???
"""
import models

class Playlist:
    # 생성자
    def __init__(self):
        self.list = []
    
    # 순회 가능한 객체로 만들기
    def __iter__(self):
        if self.list:
            return iter(self.list)
        else:
            # NoMusicInListError에 list를 매개변수 넣기
            raise models.NoMusicInListError(self.list)

    # 목록 조회
    def get_list(self):
        if self.list:
            return self.list

    # 제목 수정
    def update_title(self, id, new_title):
        for music in self.list:
            if music.id == id:
                music.title = new_title
                return
        raise models.MusicNotFoundError()

    # 재생시간 수정
    def update_track_length(self, id, new_track_length):
        for music in self.list:
            if music.id == id:
                music.track_length = new_track_length
                music.tl = f"{new_track_length // 60}:{new_track_length % 60}"
                return
        raise models.MusicNotFoundError()

    # 음악 추가
    def add_music(self, music):
        self.list.append(music)

    # 음악 검색 (제목, 가수)
    def get_music_by_keyword(self, keyword):
        result = []
        for music in self.list:
            if keyword in music.title or keyword in music.artist:
                result.append(music)
        if result:
            return result
        else:
            raise models.NoMusicInListError("검색 결과가 없습니다.")

    # 음악 검색 (가사)
    def get_music_by_lyric(self, lyric):
        result = []
        for music in self.list:
            if type(music) == models.Song and lyric in music.lyrics:
                result.append(music)
        if result:
            return result
        else:
            raise models.NoMusicInListError("검색 결과가 없습니다.")

    # 음악 삭제
    def del_music_by_id(self, id):
        for music in self.list:
            if music.id == id:
                self.list.remove(music)
                return

        

