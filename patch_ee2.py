import sys, os, re

def patch(path, *replacements):
    if not os.path.exists(path):
        print(f'[SKIP] not found: {os.path.basename(path)}')
        return
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    original = c
    for old, new in replacements:
        c = c.replace(old, new)
    if c == original:
        print(f'[WARN] no change: {os.path.basename(path)}')
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[OK]   {os.path.basename(path)}')

SRC = sys.argv[1]

# --- CheckedItem.vue ---
CHECKED = os.path.join(SRC, 'renderer', 'src', 'web', 'price-check', 'CheckedItem.vue')
patch(CHECKED,
    (
        '    <div v-if="showSupportLinks" class="mt-auto border border-dashed p-2">\n'
        '      <!-- <div class="mb-1">\n'
        '        {{ t("Support development on") }}\n'
        '        <a\n'
        '          href="https://patreon.com/awakened_poe_trade"\n'
        '          class="inline-flex align-middle animate__animated animate__fadeInRight"\n'
        '          target="_blank"\n'
        '          ><img class="inline h-5" src="/images/Patreon.svg"\n'
        '        /></a>\n'
        '      </div> -->\n'
        '      <i18n-t keypath="app.thanks_3rd_party" tag="div">\n'
        '        <a\n'
        '          href="https://poe.ninja/support"\n'
        '          target="_blank"\n'
        '          class="bg-gray-900 px-1 rounded"\n'
        '          >poe.ninja</a\n'
        '        >\n'
        '      </i18n-t>\n'
        '    </div>\n',
        ''
    ),
    ('let _showSupportLinksCounter = 0;\n', ''),
    (
        '    const showSupportLinks = ref(false);\n'
        '    const showTip = ref(0);\n'
        '    watch(\n'
        '      () => [props.item, doSearch.value],\n'
        '      ([cItem, cInteracted], [pItem]) => {\n'
        '        if (\n'
        '          _showSupportLinksCounter >= 13 &&\n'
        '          (!cInteracted || tradeAPI.value === "bulk")\n'
        '        ) {\n'
        '          showSupportLinks.value = true;\n'
        '          _showSupportLinksCounter = 0;\n'
        '        } else {\n'
        '          showSupportLinks.value = false;\n'
        '          if (\n',
        '    const showTip = ref(0);\n'
        '    watch(\n'
        '      () => [props.item, doSearch.value],\n'
        '      ([cItem, cInteracted], [pItem]) => {\n'
        '        if (false) {\n'
        '          // support links removed\n'
        '        } else {\n'
        '          if (\n'
    ),
    (
        '          if (cItem !== pItem) {\n'
        '            _showSupportLinksCounter += 1;\n'
        '          }\n'
        '        }\n',
        '        }\n'
    ),
    ('      showSupportLinks,\n', ''),
    ('<tip v-else-if="showTip"', '<tip v-if="showTip"'),
)

# --- SettingsWindow.vue ---
SW = os.path.join(SRC, 'renderer', 'src', 'web', 'settings', 'SettingsWindow.vue')
patch(SW,
    # コメントアウト済みPatreonブロック削除
    (
        '          <!-- <div\n'
        '            class="text-gray-400 text-center mt-auto pr-3 pt-4 pb-12"\n'
        '            style="max-width: fit-content; min-width: 100%"\n'
        '          >\n'
        '            <img class="mx-auto mb-1" src="/images/peepoLove2x.webp" />\n'
        '            {{ t("Support development on") }}<br />\n'
        '            <a\n'
        '              href="https://patreon.com/awakened_poe_trade"\n'
        '              class="inline-flex mt-1"\n'
        '              target="_blank"\n'
        '              ><img class="inline h-5" src="/images/Patreon.svg"\n'
        '            /></a>\n'
        '          </div> -->\n',
        ''
    ),
    # podium（ホバー表彰台）削除
    (
        '    <div :class="$style.podium" v-if="podiumVisible">\n'
        '      <div v-for="i in [2, 4, 5, 3, 1]">\n'
        '        <div\n'
        '          v-for="patron in patrons[i - 1]"\n'
        '          :key="patron.from"\n'
        '          :class="[$style.rating, $style[`rating-${patron.style}`]]"\n'
        '        >\n'
        '          {{ patron.from\n'
        '          }}{{\n'
        '            patron.months > 1\n'
        '              ? `\n'
        '          x${patron.months}`\n'
        '              : null\n'
        '          }}\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n',
        ''
    ),
    # スクロールバナー削除
    (
        '    <div\n'
        '      :class="[$style.patronsHorizontal, { invisible: podiumVisible }]"\n'
        '      :onMouseenter="showPodium"\n'
        '    >\n'
        '      <div\n'
        '        class="bg-gray-800 rounded p-1 justify-center text-center w-44 shrink-0 flex items-center"\n'
        '      >\n'
        '        {{ t("settings.thank_you") }}\n'
        '      </div>\n'
        '      <div class="overflow-x-hidden whitespace-nowrap p-1 text-base">\n'
        '        <span :class="$style.patronsLine">{{ patronsString[0] }}</span\n'
        '        ><br />\n'
        '        <span :class="$style.patronsLine">{{ patronsString[1] }}</span>\n'
        '      </div>\n'
        '    </div>\n',
        ''
    ),
    # hidePodiumトリガー削除
    (
        '      :onMouseenter="hidePodium"\n',
        '\n'
    ),
    # script: patrons/podium関連の変数・ロジック削除
    (
        '    const podiumVisible = shallowRef(false);\n'
        '    const patrons = shallowRef<Array<typeof APP_PATRONS>>([]);\n\n',
        ''
    ),
    (
        '          patrons.value = [1, 2, 3, 4, 5].map((i) =>\n'
        '            shuffle(APP_PATRONS.filter((row) => row.style === i)),\n'
        '          );\n',
        ''
    ),
    (
        '          podiumVisible.value = false;\n',
        ''
    ),
    (
        '      patrons,\n'
        '      patronsString: computed(() => {\n'
        '        return [true, false].map((firstHalf) => {\n'
        '          return patrons.value\n'
        '            .flatMap((tier) => {\n'
        '              const half = Math.ceil(tier.length / 2);\n'
        '              tier = firstHalf ? tier.slice(0, half) : tier.slice(half);\n'
        '              return tier.map((e) => e.from);\n'
        '            })\n'
        '            .reverse()\n'
        '            .join(" • ");\n'
        '        });\n'
        '      }),\n'
        '      podiumVisible,\n'
        '      showPodium() {\n'
        '        podiumVisible.value = true;\n'
        '      },\n'
        '      hidePodium() {\n'
        '        podiumVisible.value = false;\n'
        '      },\n',
        ''
    ),
    # APP_PATRONSのimport削除
    (
        'import { APP_PATRONS } from "@/assets/data";\n',
        ''
    ),
    # shuffle関数削除
    (
        'function shuffle<T>(array: T[]): T[] {\n'
        '  let currentIndex = array.length;\n'
        '  while (currentIndex !== 0) {\n'
        '    const randomIndex = Math.floor(Math.random() * currentIndex);\n'
        '    currentIndex--;\n'
        '    [array[currentIndex], array[randomIndex]] = [\n'
        '      array[randomIndex],\n'
        '      array[currentIndex],\n'
        '    ];\n'
        '  }\n'
        '  return array;\n'
        '}\n\n',
        ''
    ),
)

# --- about.vue ---
ABOUT = os.path.join(SRC, 'renderer', 'src', 'web', 'settings', 'about.vue')
patch(ABOUT,
    (
        '    <div class="text-center mt-auto py-8">\n'
        '      <p>\n'
        '        {{ t("app.contact_me") }} <br /><span\n'
        '          class="font-sans text-gray-500 select-all"\n'
        '          >&lt;@340233612064718851&gt;</span\n'
        '        >\n'
        '      </p>\n'
        '      <ul class="flex gap-4">\n'
        '        <li>\n'
        '          <img class="rounded inline" src="/images/dc_reddit.png" />\n'
        '          <a\n'
        '            class="border-b"\n'
        '            href="https://old.reddit.com/r/pathofexile2"\n'
        '            target="_blank"\n'
        '            >r/pathofexile</a\n'
        '          >\n'
        '        </li>\n'
        '        <li>\n'
        '          <img class="rounded inline" src="/images/discord.png" />\n'
        '          <a\n'
        '            class="border-b"\n'
        '            href="https://discord.gg/pathofexile"\n'
        '            target="_blank"\n'
        '            >pathofexile</a\n'
        '          >\n'
        '        </li>\n'
        '      </ul>\n'
        '    </div>\n',
        ''
    ),
)

# --- AppTray.ts 日本語化 ---
TRAY = os.path.join(SRC, 'main', 'src', 'AppTray.ts')
patch(TRAY,
    ('label: "Settings/League"', 'label: "設定/リーグ"'),
    (
        'message: `Open Path of Exile 2 and press "${this.overlayKey}". Click on the button with cog icon there.`',
        'message: `Path of Exile 2 を起動して "${this.overlayKey}" を押してください。歯車アイコンのボタンから設定できます。`'
    ),
    ('label: "Open in Browser"', 'label: "ブラウザで開く"'),
    ('label: "Open config folder"', 'label: "設定フォルダを開く"'),
    ('label: "Quit"', 'label: "終了"'),
)

# --- ja/app_i18n.json 未翻訳キーを追加 ---
import json as _json

JA_JSON = os.path.join(SRC, 'renderer', 'public', 'data', 'ja', 'app_i18n.json')
if os.path.exists(JA_JSON):
    with open(JA_JSON, 'r', encoding='utf-8') as _f:
        _ja = _json.load(_f)

    NEW_TRANSLATIONS = {
        "app": {
            "deprecated": "この機能は非推奨となり、アップデート {0} で削除されます"
        },
        "item": {
            "find_same_price": "フィルター",
            "find_same_price_type": "フィルター:",
            "price": "価格のみ",
            "price_and_item": "価格とアイテム",
            "open_on_craftofexile": "Craft of Exile でベースアイテムを開く",
            "mod_desecrated": "Desecrated",
            "not_sanctified": "Not Sanctified",
            "has_elemental_affix": "Any",
            "has_elemental_fire_affix": "Fire",
            "has_elemental_cold_affix": "Cold",
            "has_elemental_lightning_affix": "Lightning",
            "ascendancy_points": "ポイント: {0}"
        },
        "item_category": {
            "armour_focus": "Focus",
            "map_tablet": "Tablet"
        },
        "filters": {
            "selected_open_runes": "{0} / {1}、空き",
            "selected_full_runes": "Runes フル",
            "empty_rune_socket": "空き Rune ソケット",
            "hide_low_ilvl": "アイテムレベルが低すぎて全 mod をロールできません",
            "hide_not_max_level": "最大レベルでないスキルは価値がほとんどありません",
            "hide_for_map": "ほとんどのマップ mod に価値はありません",
            "hide_revives": "0以外かつExaltしたくない場合のみ選択？",
            "tag_sanctum": "Sanctum",
            "tag_skill": "スキル",
            "tag_mutated": "Mutated",
            "fill_rune_iron": "Runes を補充（Iron）",
            "hybrid_note": "hybrid mod の可能性があるため、Tier が正確でない場合があります"
        },
        "online_filter": {
            "ratio_tooltip": "ローカルでのソートに使用するレート\nトレードサイトのデフォルトは 7.5:1"
        },
        "notepad": {
            "name": "メモ帳",
            "placeholder": "ここにメモを入力…",
            "width": "幅:"
        },
        "trade_result": {
            "normalized": "N-価格",
            "gem_sockets": "ソケット",
            "results_warn_tooltip": "オンラインフィルターで「Exalted のみ」を有効にしてください。この警告は設定で無効にできます。",
            "results_warn_title": "価格が高すぎる可能性があります",
            "results_warn_message": "トレードサイトが {0} ～ {1} ex の結果を非表示にしています",
            "likely_price_fixed": "非標準通貨が多数: ",
            "filter_exalt_divine": "Exalt/Divine でフィルター",
            "highest_volume": "最高取引量:"
        },
        "settings": {
            "preferred_trade_site": "優先トレードサイト",
            "enable_alphas": "実験的機能を有効にする",
            "alpha_library": "アイテムデータ収集",
            "read_client_log": "Client.txt ファイルの読み取りを許可する",
            "client_log_explain": "Client.txt ログファイルにはデバッグ情報とチャットログが含まれています。ゾーン変更やプレイヤーのレベルアップの検出に使用されます。"
        },
        "price_check": {
            "show_suggest_warning": "価格チェック誤り警告",
            "show_suggest_warning_none": "無効",
            "show_suggest_warning_warn": "警告を表示",
            "show_suggest_warning_help": "警告とヘルプを表示",
            "always_show_tier": "常に Tier を表示",
            "remember_ratio": "通貨レートを記憶する",
            "remember_listing": "リスティング種別を記憶する",
            "open_editor_above": "Rune ソケット選択を上方向に開く",
            "core_currency": "基本通貨:",
            "show_volume": "Currency Exchange の1時間あたりの取引量を表示:"
        },
        "leveling": {
            "name": "レベリング",
            "enable_read_client_logs": "レベリングウィジェットにはクライアントログの読み取り許可が必要です",
            "exp_tracking": "経験値トラッカー",
            "show_exp": "経験値獲得率を表示",
            "exp_tracking_help_tldr": "要約: 「Over」を 0 か 1 に保つようにしましょう",
            "exp_tracking_help": "経験値トラッカーは現在レベル、経験値倍率、アンダーレベルまでの距離を表示します。オーバーレベル時はすぐにペナルティが適用され、⌊ level/16 + 3 ⌋ レベル以上低いとアンダーレベルペナルティが発生します。「Over」はセーフゾーン下限からの超過レベル数で、通常 0 か 1 であればペナルティなしで最高レベルの敵を倒せています",
            "exp_inspire": "参考: ",
            "exp_astrict": "※レベル95超、またはモンスターレベル70超の場合、もしくは経験値獲得率が100%でない場合、経験値獲得率の表示が正確でない可能性があります。",
            "reparse": "解析済みログデータを再生成"
        },
        "library": {
            "name": "ライブラリ",
            "log_item_key": "アイテムをCSVに記録",
            "output_file": "CSV出力パス",
            "output_folder": "出力フォルダ",
            "output_file_help": "情報テキスト",
            "record_count": "セッションロール数:"
        }
    }

    def deep_merge(base, additions):
        for k, v in additions.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                deep_merge(base[k], v)
            elif k not in base:
                base[k] = v

    deep_merge(_ja, NEW_TRANSLATIONS)

    with open(JA_JSON, 'w', encoding='utf-8') as _f:
        _json.dump(_ja, _f, ensure_ascii=False, indent=2)
    print('[OK]   ja/app_i18n.json (69 keys added)')
else:
    print(f'[SKIP] ja/app_i18n.json not found')

# --- crowdin.yml / FUNDING.yml ---
for f in [os.path.join(SRC, 'crowdin.yml'), os.path.join(SRC, '.github', 'FUNDING.yml')]:
    if os.path.exists(f):
        os.remove(f)
        print(f'[OK]   deleted: {os.path.basename(f)}')

print('パッチ完了')
