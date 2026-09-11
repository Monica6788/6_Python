"""
    사용자 메뉴 루프 진입점
"""
import models
import playlist

menulist = """
1. 목록 조회
2. 음악 추가
3. 음악 검색
4. 가사 검색
0. 종료
"""

in_list_menulist = """
1. 제목 수정
2. 재생시간 수정
3. 음악 삭제
"""

add_menulist = """
1. 음악 (가사 없음)
2. 노래
3. 팟캐스트
"""

my_list = playlist.Playlist()

while True:
    try:
        print(menulist)
        menu = int(input("메뉴를 선택하세요: "))
        match menu:
            case 1:
                # 목록 조회
                for music in my_list:
                    print(music)
                id = int(input("곡 번호를 입력하세요: "))
                now_playing = None
                for music in my_list.get_list():
                    if music.id == id:
                        now_playing = music
                        break
                if now_playing:
                    print(now_playing.play())
                    print("-" * 30)
                else:
                    print("재생 오류입니다.")
                    continue
                print(in_list_menulist)
                in_list_menu = int(input("메뉴를 선택하세요: "))
                match in_list_menu:
                    # 제목 수정
                    case 1:
                        new_title = input("새로운 제목을 입력하세요: ")
                        my_list.update_title(id, new_title)
                        print(f"수정이 완료되었습니다.")
                    # 재생시간 수정
                    case 2:
                        new_track_length = int(input("재생시간(초)를 입력하세요: "))
                        my_list.update_track_length(id, new_track_length)
                        print(f"수정이 완료되었습니다.")
                    # 음악 삭제
                    case 3:
                        answer = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()
                        if answer == "y":
                            my_list.del_music_by_id(id)
                        elif answer == "n":
                            continue
                        else:
                            print("잘못 누르셨습니다.")
            # 음악 추가
            case 2:
                print(add_menulist)
                add_menu = int(input("추가할 음악의 유형을 선택하세요: "))
                title = input("제목을 입력하세요: ")
                artist = input("아티스트를 입력하세요 (생략 가능): ")
                track_length = input("재생시간(초)를 입력하세요 (생략 가능): ")
                if track_length.strip() == "":
                    track_length = 0
                else:
                    track_length = int(track_length)
                match add_menu:
                    # Music 클래스 객체 추가
                    case 1: 
                        my_list.add_music(models.Music(title, artist, track_length))
                        print("음악이 추가되었습니다.")
                    # Song 클래스 객체 추가
                    case 2:
                        lyrics = input("가사를 입력하세요:")
                        my_list.add_music(models.Song(title, artist, track_length, lyrics))
                        print("노래가 추가되었습니다.")
                    # Podcast 클래스 객체 추가
                    case 3:
                        host = input("호스트를 입력하세요:")
                        ep_num = int(input("에피소드 번호를 입력하세요: "))
                        my_list.add_music(models.Podcast(title, artist, track_length, host, ep_num))
            # 음악 검색 (제목 또는 아티스트)
            case 3:
                keyword = input("검색어를 입력하세요 (제목/아티스트): ")
                result = my_list.get_music_by_keyword(keyword)
                for music in result:
                    print(music)
            # 가사 검색
            case 4:
                lyric = input("검색어를 입력하세요 (가사): ")
                result = my_list.get_music_by_lyric(lyric)
                for music in result:
                    print(music)
            # 종료
            case 0:
                print("이용해주셔서 감사합니다.")
                break
    except ValueError as ve:
        print("숫자만 입력할 수 있습니다.")
    except models.MusicNotFoundError as mnfe:
        print(mnfe)
    except models.DuplicateMusicError as dme:
        print(dme)
    except models.NoMusicInListError as nmile:
        print(nmile)
    except Exception as e:
        print("알 수 없는 오류입니다. 프로그램을 재시작해주세요.")

